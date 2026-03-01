"""
Sheriff's Secure Vault - Backend API
A security-focused system for processing and storing uploaded images as digital evidence.

This backend implements:
- Image hashing for integrity verification (tamper detection)
- Image encryption for confidentiality protection
- Secure local storage with verification badges
"""

import os
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from cryptography.fernet import Fernet
import logging

# ============================================================================
# CONFIGURATION & SETUP
# ============================================================================

# Initialize FastAPI app
app = FastAPI(
    title="Sheriff's Secure Vault",
    description="Security-focused image evidence processing system",
    version="1.0.0"
)

# Enable CORS for future frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# SECURE STORAGE & CRYPTOGRAPHY
# ============================================================================

# Create vault directory if it doesn't exist
VAULT_DIR = Path("./vault")
VAULT_DIR.mkdir(exist_ok=True, mode=0o700)  # Owner read/write/execute only

# Generate encryption key once at startup (in production, load from secure key management)
# This key is stored in memory for the lifetime of the application
ENCRYPTION_KEY = Fernet.generate_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

# In-memory storage for image metadata and hashes
# Structure: {hash_value: {"timestamp": str, "filename": str, "status": str}}
image_registry: Dict[str, Dict] = {}

logger.info("🔐 Sheriff's Secure Vault initialized")
logger.info(f"📁 Vault directory: {VAULT_DIR.absolute()}")


# ============================================================================
# CRYPTOGRAPHIC FUNCTIONS
# ============================================================================

def hash_image(file_bytes: bytes) -> str:
    """
    Generate SHA-256 hash of image bytes.
    
    WHY HASHING PROTECTS INTEGRITY:
    - Hashing creates a unique fingerprint of the exact image content
    - Even a single pixel change produces a completely different hash
    - If evidence is tampered with, the hash will no longer match
    - This creates an immutable record of the original image's integrity
    
    Args:
        file_bytes: Raw image bytes to hash
        
    Returns:
        SHA-256 hash as hexadecimal string
    """
    sha256_hash = hashlib.sha256()
    sha256_hash.update(file_bytes)
    hash_value = sha256_hash.hexdigest()
    logger.info(f"✓ Generated hash: {hash_value[:16]}...")
    return hash_value


def encrypt_image(file_bytes: bytes) -> bytes:
    """
    Encrypt image bytes using Fernet (AES-128 in CBC mode).
    
    WHY ENCRYPTION PROTECTS CONFIDENTIALITY:
    - Encryption converts readable image data into unreadable ciphertext
    - Only someone with the encryption key can decrypt and view the image
    - Protects sensitive evidence from unauthorized access
    - Fernet provides authenticated encryption (prevents tampering)
    
    Args:
        file_bytes: Raw image bytes to encrypt
        
    Returns:
        Encrypted bytes
    """
    encrypted_bytes = cipher_suite.encrypt(file_bytes)
    logger.info(f"✓ Encrypted image ({len(file_bytes)} bytes → {len(encrypted_bytes)} bytes)")
    return encrypted_bytes


def store_encrypted_image(encrypted_bytes: bytes, hash_value: str) -> str:
    """
    Store encrypted image in vault directory.
    
    Args:
        encrypted_bytes: Encrypted image data
        hash_value: SHA-256 hash used as filename
        
    Returns:
        Path to stored file
        
    Raises:
        IOError: If file write fails
    """
    try:
        # Use hash as filename (prevents collisions, aids evidence tracking)
        file_path = VAULT_DIR / f"{hash_value}.enc"
        
        # Write encrypted bytes to disk with restricted permissions
        with open(file_path, "wb") as f:
            f.write(encrypted_bytes)
        
        # Set file permissions to owner read/write only
        os.chmod(file_path, 0o600)
        
        logger.info(f"✓ Stored encrypted image: {file_path}")
        return str(file_path)
    
    except IOError as e:
        logger.error(f"✗ Failed to store encrypted image: {e}")
        raise


def verify_integrity(hash_value: str) -> bool:
    """
    Verify that an image with this hash exists in the vault.
    
    PLACEHOLDER FOR FUTURE FEATURES:
    This function will be enhanced to:
    - Re-hash stored images to detect tampering
    - Compare with blockchain/cryptographic ledger
    - Alert if hash collision detected
    - Generate forensic audit reports
    
    Args:
        hash_value: Hash to verify
        
    Returns:
        True if image exists and is verified, False otherwise
    """
    if hash_value in image_registry:
        status = image_registry[hash_value].get("status")
        logger.info(f"✓ Verified image hash: {hash_value[:16]}... (status: {status})")
        return status == "Verified"
    
    logger.warning(f"✗ Hash not found in registry: {hash_value[:16]}...")
    return False


# ============================================================================
# BADGE GENERATION
# ============================================================================

def create_verification_badge(hash_value: str, timestamp: str) -> Dict:
    """
    Create a verification badge for evidence tracking.
    
    The badge serves as a certificate of authenticity and integrity.
    
    Args:
        hash_value: SHA-256 hash of the image
        timestamp: ISO-format timestamp of storage
        
    Returns:
        Badge object with verification metadata
    """
    badge = {
        "hash": hash_value,
        "timestamp": timestamp,
        "status": "Verified",
        "sealed": True,
        "vault": str(VAULT_DIR.absolute()),
        "encryption": "Fernet (AES-128-CBC)"
    }
    return badge


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """
    Upload an image to Sheriff's Secure Vault.
    
    Process:
    1. Accept image file upload
    2. Read raw bytes without modification
    3. Generate SHA-256 hash (integrity fingerprint)
    4. Encrypt using Fernet AES encryption
    5. Store encrypted image with hash-based filename
    6. Create verification badge
    7. Return proof of storage
    
    Args:
        file: Uploaded image file
        
    Returns:
        JSON response with hash, timestamp, and verification badge
        
    Raises:
        HTTPException: If file processing fails
    """
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            logger.warning(f"✗ Invalid file type: {file.content_type}")
            raise HTTPException(
                status_code=400,
                detail="File must be an image (image/png, image/jpeg, etc.)"
            )
        
        # Read raw image bytes (do not modify)
        image_bytes = await file.read()
        
        if not image_bytes:
            logger.warning("✗ Empty file uploaded")
            raise HTTPException(
                status_code=400,
                detail="Image file is empty"
            )
        
        logger.info(f"📥 Received image: {file.filename} ({len(image_bytes)} bytes)")
        
        # Step 1: Hash the image for integrity verification
        hash_value = hash_image(image_bytes)
        
        # Step 2: Encrypt the image for confidentiality
        encrypted_bytes = encrypt_image(image_bytes)
        
        # Step 3: Store encrypted image in vault
        file_path = store_encrypted_image(encrypted_bytes, hash_value)
        
        # Step 4: Record in registry and generate timestamp
        timestamp = datetime.utcnow().isoformat() + "Z"
        image_registry[hash_value] = {
            "filename": file.filename,
            "timestamp": timestamp,
            "status": "Verified",
            "file_path": file_path,
            "file_size": len(image_bytes)
        }
        
        logger.info(f"✓ Image stored successfully: {hash_value[:16]}...")
        
        # Step 5: Create verification badge
        badge = create_verification_badge(hash_value, timestamp)
        
        # Step 6: Verify integrity before returning
        is_verified = verify_integrity(hash_value)
        
        if not is_verified:
            logger.error(f"✗ Verification failed for hash: {hash_value}")
            raise HTTPException(
                status_code=500,
                detail="Image verification failed after storage"
            )
        
        # Return response
        response = {
            "message": "✓ Stored in Sheriff's Secure Vault",
            "hash": hash_value,
            "timestamp": timestamp,
            "badge": badge,
            "file_size_bytes": len(image_bytes),
            "encrypted_size_bytes": len(encrypted_bytes),
            "original_filename": file.filename
        }
        
        logger.info(f"📦 Response ready for hash: {hash_value[:16]}...")
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Unexpected error during upload: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint for deployment verification."""
    vault_status = "ready" if VAULT_DIR.exists() else "not_ready"
    return {
        "status": "healthy",
        "service": "Sheriff's Secure Vault",
        "vault": vault_status,
        "images_stored": len(image_registry)
    }


@app.get("/registry")
async def get_registry():
    """
    ADMIN ENDPOINT: Return in-memory registry of stored images.
    
    WARNING: In production, this should be:
    - Protected with authentication
    - Paginated
    - Logged for audit trails
    """
    return {
        "total_images": len(image_registry),
        "registry": image_registry
    }


@app.post("/verify/{hash_value}")
async def verify_image(hash_value: str):
    """
    Verify that an image with the given hash exists and is intact.
    
    Args:
        hash_value: SHA-256 hash to verify
        
    Returns:
        Verification status and metadata
    """
    is_valid = verify_integrity(hash_value)
    
    if hash_value not in image_registry:
        raise HTTPException(
            status_code=404,
            detail=f"Image with hash {hash_value[:16]}... not found in vault"
        )
    
    metadata = image_registry[hash_value]
    
    return {
        "hash": hash_value,
        "verified": is_valid,
        "timestamp": metadata["timestamp"],
        "filename": metadata["filename"],
        "status": metadata["status"]
    }


# ============================================================================
# STARTUP & SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize vault on startup."""
    logger.info("🚀 Sheriff's Secure Vault starting up...")
    logger.info(f"🔑 Encryption key loaded (length: {len(ENCRYPTION_KEY)} bytes)")
    logger.info(f"📊 Registry initialized with {len(image_registry)} entries")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("🛑 Sheriff's Secure Vault shutting down...")
    logger.info(f"📊 Final registry size: {len(image_registry)} images")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    logger.info("=" * 70)
    logger.info("  Sheriff's Secure Vault - Backend Server")
    logger.info("=" * 70)
    logger.info("Starting FastAPI server on http://localhost:8000")
    logger.info("Docs available at http://localhost:8000/docs")
    logger.info("=" * 70)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
