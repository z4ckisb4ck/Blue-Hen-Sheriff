# Sheriff's Secure Vault - Backend API

A security-focused backend system for processing and storing uploaded images as digital evidence. This is a hackathon project demonstrating cryptographic integrity verification and confidentiality protection.

## 🔐 Security Features

### Integrity Protection (Hashing)
- **SHA-256 hashing** creates a unique fingerprint of each image
- Any modification (even 1 pixel) produces a completely different hash
- Serves as proof that evidence has not been tampered with
- Enables future auditing and forensic analysis

### Confidentiality Protection (Encryption)
- **Fernet encryption** (AES-128 in CBC mode) protects image content
- Encrypted images are unreadable without the decryption key
- Prevents unauthorized access to sensitive evidence
- Authenticated encryption detects tampering attempts

### Secure Storage
- Encrypted images stored with hash-based filenames
- File permissions restricted to owner only (0o600)
- In-memory registry tracks all stored evidence
- Verification badges provide proof of authenticity

## 📁 Project Structure

```
backend/
├── sheriffs_vault_main.py      # Main FastAPI application
├── sheriffs_vault_requirements.txt
└── vault/                       # Auto-created directory for encrypted images
    └── [hash].enc               # Encrypted image files
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r sheriffs_vault_requirements.txt
```

### 2. Run the Server

```bash
python sheriffs_vault_main.py
```

The API will start at `http://localhost:8000`

### 3. Access API Documentation

Open your browser to `http://localhost:8000/docs` for interactive API documentation (Swagger UI)

## 📡 API Endpoints

### POST `/upload`
Upload an image to the secure vault.

**Request:**
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "accept: application/json" \
  -F "file=@evidence.jpg"
```

**Response:**
```json
{
  "message": "✓ Stored in Sheriff's Secure Vault",
  "hash": "a3f1c2d4e5b8c9d1f2e3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b",
  "timestamp": "2025-02-28T14:32:00.123456Z",
  "badge": {
    "hash": "a3f1c2d4e5b8c9d1f2e3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b",
    "timestamp": "2025-02-28T14:32:00.123456Z",
    "status": "Verified",
    "sealed": true,
    "vault": "/absolute/path/to/vault",
    "encryption": "Fernet (AES-128-CBC)"
  },
  "file_size_bytes": 2048576,
  "encrypted_size_bytes": 2048592,
  "original_filename": "evidence.jpg"
}
```

### GET `/health`
Check vault status.

**Request:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Sheriff's Secure Vault",
  "vault": "ready",
  "images_stored": 3
}
```

### GET `/registry`
Retrieve in-memory registry of all stored images.

**Request:**
```bash
curl http://localhost:8000/registry
```

**Response:**
```json
{
  "total_images": 1,
  "registry": {
    "a3f1c2d4e5b8c9d1f2e3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b": {
      "filename": "evidence.jpg",
      "timestamp": "2025-02-28T14:32:00.123456Z",
      "status": "Verified",
      "file_path": "./vault/a3f1c2d4e5b8c9d1f2e3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b.enc",
      "file_size": 2048576
    }
  }
}
```

### POST `/verify/{hash_value}`
Verify an image exists and is intact.

**Request:**
```bash
curl -X POST "http://localhost:8000/verify/a3f1c2d4e5b8c9d1f2e3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b"
```

**Response:**
```json
{
  "hash": "a3f1c2d4e5b8c9d1f2e3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b",
  "verified": true,
  "timestamp": "2025-02-28T14:32:00.123456Z",
  "filename": "evidence.jpg",
  "status": "Verified"
}
```

## 🔑 Key Implementation Details

### Encryption Key Management
- Single Fernet key generated at server startup
- Stored in memory for the lifetime of the process
- **Production note:** Use secure key management (AWS KMS, HashiCorp Vault, etc.)

### Hash-Based Storage
- Images stored with hash as filename: `{hash}.enc`
- Prevents filename collisions
- Aids evidence tracking and audit trails
- Hash lookup is O(1) for fast verification

### In-Memory Registry
- Dictionary-based storage for image metadata
- No database required for MVP/hackathon
- Tracks: timestamp, filename, verification status, file path, size
- **Production note:** Migrate to database with query capabilities

### Verification Workflow
```
1. User uploads image
2. Image hashed (SHA-256) for integrity fingerprint
3. Image encrypted (Fernet/AES) for confidentiality
4. Encrypted image stored with hash filename
5. Metadata stored in registry
6. Verification badge generated
7. Hash returned to user as proof of receipt
```

## 🛡️ Security Considerations

### Current Implementation (MVP)
✅ Proper encryption using Fernet (AES-128-CBC)
✅ Cryptographic hashing with SHA-256
✅ File permissions restricted (0o600)
✅ Error handling and logging
✅ Input validation (file type checking)

### Production Enhancements Needed
⚠️ **Key Management:** Use AWS KMS, HashiCorp Vault, or similar
⚠️ **Authentication:** Implement JWT or OAuth2 for API access control
⚠️ **Authorization:** Role-based access control (RBAC) for registry/verification
⚠️ **Audit Logging:** Track all access attempts with timestamps and user IDs
⚠️ **Database:** Replace in-memory registry with persistent storage
⚠️ **HTTPS:** Use TLS/SSL for encrypted transport
⚠️ **Rate Limiting:** Protect against DOS attacks
⚠️ **Tampering Detection:** Compare re-hashed images against stored hashes

## 📊 Testing the Backend

### Using curl (command line)

**Upload an image:**
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@/path/to/image.jpg"
```

**Check health:**
```bash
curl http://localhost:8000/health
```

**View registry:**
```bash
curl http://localhost:8000/registry
```

**Verify an image:**
```bash
curl -X POST "http://localhost:8000/verify/[paste-hash-here]"
```

### Using Python

```python
import requests

# Upload
with open("image.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post("http://localhost:8000/upload", files=files)
    result = response.json()
    print(f"Hash: {result['hash']}")
    print(f"Verified: {result['badge']['status']}")

# Verify
hash_value = result['hash']
response = requests.post(f"http://localhost:8000/verify/{hash_value}")
print(response.json())
```

## 🔄 Workflow Examples

### Example 1: Evidence Submission
```
1. Detective uploads crime scene photo
2. System returns SHA-256 hash + verification badge
3. Detective stores hash in incident report
4. Later, detective can verify hash hasn't changed
5. Chain of custody is cryptographically proven
```

### Example 2: Integrity Verification
```
1. Someone claims to have the original image
2. We re-hash their image
3. Compare: new hash vs stored hash
4. If different → image was modified
5. If identical → image is unaltered
```

## 📝 Logging

The application logs all operations with timestamps:

```
INFO:__main__:✓ Generated hash: a3f1c2d4e5b8...
INFO:__main__:✓ Encrypted image (2048576 bytes → 2048592 bytes)
INFO:__main__:✓ Stored encrypted image: ./vault/a3f1c2d4.enc
INFO:__main__:✓ Verified image hash: a3f1c2d4... (status: Verified)
```

Monitor logs for:
- ✓ = Successful operation
- ✗ = Error or security event
- 📥 = File received
- 📦 = Response prepared
- 🔐 = Security-related

## 🚨 Error Handling

The API returns appropriate HTTP status codes:

- **200 OK:** Upload successful
- **400 Bad Request:** Invalid file type, empty file
- **404 Not Found:** Hash not found in registry
- **500 Internal Server Error:** Storage or encryption failure

Example error response:
```json
{
  "detail": "File must be an image (image/png, image/jpeg, etc.)"
}
```

## 🔮 Future Enhancements

### Phase 2 (Database)
- [ ] PostgreSQL backend for persistent storage
- [ ] Queryable registry (filter by date, filename, etc.)
- [ ] Audit logging table

### Phase 3 (Authentication)
- [ ] JWT tokens for API access
- [ ] User accounts and permissions
- [ ] Multi-tenant support

### Phase 4 (Advanced Security)
- [ ] Hardware security module (HSM) integration
- [ ] Blockchain-based ledger for tamper evidence
- [ ] Image decryption endpoint with access logging
- [ ] Forensic report generation

### Phase 5 (Frontend)
- [ ] Web interface for evidence upload
- [ ] Visual verification badge display
- [ ] Evidence timeline and search

## 📄 License

This is a hackathon project. Use for educational and authorized purposes only.

## ⚖️ Legal Notice

Ensure all image data is:
- Legally obtained
- Handled in compliance with data protection laws
- Properly authorized for processing
- Stored securely with appropriate access controls

---

**Built with 🛡️ for secure evidence handling**
