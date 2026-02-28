
// Animation and interactivity for Blue Hen Sheriff
window.onload = function() {
	const canvas = document.getElementById('wildwest-canvas');
	if (!canvas) return;
	const ctx = canvas.getContext('2d');

	// Animation state
	let frame = 0;
	let horseX = 60;
	let personX = horseX + 120; // Person always ahead of horse

	function drawBackground() {
		// Sky (blue)
		ctx.fillStyle = '#7ecbff'; // light blue
		ctx.fillRect(0, 0, canvas.width, canvas.height);
		// Clouds
		// More clouds, distributed across the sky
		drawCloud(ctx, 100, 55, 38, 18);
		drawCloud(ctx, 180, 60, 32, 18);
		drawCloud(ctx, 260, 48, 44, 20);
		drawCloud(ctx, 340, 38, 40, 22);
		drawCloud(ctx, 420, 60, 36, 16);
		drawCloud(ctx, 500, 50, 30, 14);
		drawCloud(ctx, 580, 70, 28, 14);
		drawCloud(ctx, 650, 45, 34, 16);
		// Sun (prominent, left side)
		ctx.save();
		ctx.beginPath();
		ctx.arc(60, 80, 38, 0, 2 * Math.PI);
		ctx.fillStyle = '#FFD700';
		ctx.shadowColor = '#FFD700';
		ctx.shadowBlur = 32;
		ctx.globalAlpha = 0.95;
		ctx.fill();
		ctx.globalAlpha = 1;
		ctx.shadowBlur = 0;
		ctx.restore();
		// Draw a cartoon cloud at (x, y) with width w and height h using multiple overlapping ellipses
		function drawCloud(ctx, x, y, w, h) {
			ctx.save();
			ctx.fillStyle = '#fff';
			ctx.globalAlpha = 0.92;
			// Main body
			ctx.beginPath();
			ctx.ellipse(x, y, w, h, 0, 0, 2 * Math.PI);
			ctx.ellipse(x - w * 0.4, y + h * 0.1, w * 0.6, h * 0.7, 0, 0, 2 * Math.PI);
			ctx.ellipse(x + w * 0.4, y + h * 0.1, w * 0.6, h * 0.7, 0, 0, 2 * Math.PI);
			ctx.ellipse(x - w * 0.2, y - h * 0.3, w * 0.5, h * 0.5, 0, 0, 2 * Math.PI);
			ctx.ellipse(x + w * 0.2, y - h * 0.3, w * 0.5, h * 0.5, 0, 0, 2 * Math.PI);
			ctx.fill();
			ctx.globalAlpha = 1;
			ctx.restore();
		}
		// Ground
		ctx.fillStyle = '#e2b07a';
		ctx.fillRect(0, canvas.height * 0.7, canvas.width, canvas.height * 0.3);

		// --- Wild West Buildings ---
		// Building 1: Barn (left)
		ctx.save();
		ctx.fillStyle = '#a97c50';
		ctx.strokeStyle = '#6e4b2a';
		ctx.lineWidth = 4;
		ctx.fillRect(40, 180, 110, 120);
		ctx.strokeRect(40, 180, 110, 120);
		// Barn roof
		ctx.beginPath();
		ctx.moveTo(30, 180);
		ctx.lineTo(95, 140);
		ctx.lineTo(160, 180);
		ctx.closePath();
		ctx.fillStyle = '#7a5a36';
		ctx.fill();
		ctx.stroke();
		// Barn door
		ctx.fillStyle = '#6e4b2a';
		ctx.fillRect(80, 240, 30, 60);
		ctx.strokeRect(80, 240, 30, 60);
		ctx.restore();

		// Building 2: Sheriff (with star)
		ctx.save();
		ctx.fillStyle = '#bfa06a';
		ctx.strokeStyle = '#6e4b2a';
		ctx.lineWidth = 4;
		ctx.fillRect(170, 160, 120, 140);
		ctx.strokeRect(170, 160, 120, 140);
		// Roof
		ctx.beginPath();
		ctx.moveTo(160, 160);
		ctx.lineTo(230, 120);
		ctx.lineTo(290, 160);
		ctx.closePath();
		ctx.fillStyle = '#7a5a36';
		ctx.fill();
		ctx.stroke();
		// Star
		ctx.save();
		ctx.translate(230, 150);
		ctx.rotate(Math.PI / 10);
		ctx.beginPath();
		for (let i = 0; i < 5; i++) {
			ctx.lineTo(0, 12);
			ctx.translate(0, 12);
			ctx.rotate((Math.PI * 2) / 5);
			ctx.lineTo(0, -12);
			ctx.translate(0, -12);
			ctx.rotate(-(Math.PI * 6) / 5);
		}
		ctx.closePath();
		ctx.fillStyle = '#FFD700';
		ctx.fill();
		ctx.restore();
		ctx.restore();

		// Building 3: Home (center)
		ctx.save();
		ctx.fillStyle = '#e2cfa7';
		ctx.strokeStyle = '#6e4b2a';
		ctx.lineWidth = 4;
		ctx.fillRect(310, 140, 120, 160);
		ctx.strokeRect(310, 140, 120, 160);
		// Roof
		ctx.beginPath();
		ctx.moveTo(300, 140);
		ctx.lineTo(370, 90);
		ctx.lineTo(430, 140);
		ctx.closePath();
		ctx.fillStyle = '#bfa06a';
		ctx.fill();
		ctx.stroke();
		ctx.restore();

		// Building 4: Resources (right of center)
		ctx.save();
		ctx.fillStyle = '#e2b07a';
		ctx.strokeStyle = '#6e4b2a';
		ctx.lineWidth = 4;
		ctx.fillRect(450, 170, 110, 130);
		ctx.strokeRect(450, 170, 110, 130);
		// Roof
		ctx.beginPath();
		ctx.moveTo(445, 170);
		ctx.lineTo(505, 130);
		ctx.lineTo(565, 170);
		ctx.closePath();
		ctx.fillStyle = '#bfa06a';
		ctx.fill();
		ctx.stroke();
		ctx.restore();

		// Building 5: Saloon/Schedule (far right)
		ctx.save();
		ctx.fillStyle = '#e2cfa7';
		ctx.strokeStyle = '#6e4b2a';
		ctx.lineWidth = 4;
		ctx.fillRect(580, 160, 110, 140);
		ctx.strokeRect(580, 160, 110, 140);
		// Roof
		ctx.beginPath();
		ctx.moveTo(575, 160);
		ctx.lineTo(635, 120);
		ctx.lineTo(695, 160);
		ctx.closePath();
		ctx.fillStyle = '#bfa06a';
		ctx.fill();
		ctx.stroke();
		ctx.restore();
	}

	// Draw a flat, cartoon-style person running (to match provided image)
	function drawPerson(x, y) {
		ctx.save();
		// Legs
		ctx.lineWidth = 5;
		ctx.strokeStyle = '#6e4b2a';
		ctx.beginPath();
		ctx.moveTo(x - 7, y + 32);
		ctx.lineTo(x - 7 + Math.sin(frame / 5) * 8, y + 52);
		ctx.moveTo(x + 7, y + 32);
		ctx.lineTo(x + 7 - Math.sin(frame / 5) * 8, y + 52);
		ctx.stroke();
		// Body (rectangle, shirt)
		ctx.fillStyle = '#e2b07a';
		ctx.strokeStyle = '#6e4b2a';
		ctx.lineWidth = 4;
		ctx.beginPath();
		ctx.rect(x - 13, y + 2, 26, 30);
		ctx.fill();
		ctx.stroke();
		// Head (circle)
		ctx.beginPath();
		ctx.arc(x, y - 10, 13, 0, 2 * Math.PI);
		ctx.fillStyle = '#f7d7b6';
		ctx.fill();
		ctx.stroke();
		// Eyes
		ctx.beginPath();
		ctx.arc(x - 5, y - 13, 2, 0, 2 * Math.PI);
		ctx.arc(x + 5, y - 13, 2, 0, 2 * Math.PI);
		ctx.fillStyle = '#222';
		ctx.fill();
		// Smile
		ctx.beginPath();
		ctx.arc(x, y - 7, 4, 0, Math.PI);
		ctx.lineWidth = 2;
		ctx.strokeStyle = '#a0522d';
		ctx.stroke();
		// Arms
		ctx.lineWidth = 5;
		ctx.strokeStyle = '#e2b07a';
		ctx.beginPath();
		ctx.moveTo(x - 13, y + 10);
		ctx.lineTo(x - 30 + Math.sin(frame / 7) * 6, y + 2);
		ctx.moveTo(x + 13, y + 10);
		ctx.lineTo(x + 30 - Math.sin(frame / 7) * 6, y + 2);
		ctx.stroke();
		ctx.restore();
	}

	// Draw a flat, cartoon-style sheriff hen (police blue, hat, badge, bold outline)
	function drawSheriffHen(x, y) {
		ctx.save();
		// Body (blue, oval)
		ctx.beginPath();
		ctx.ellipse(x, y, 20, 14, 0, 0, 2 * Math.PI);
		ctx.fillStyle = '#1e90ff';
		ctx.fill();
		ctx.lineWidth = 4;
		ctx.strokeStyle = '#6e4b2a';
		ctx.stroke();
		// Head (white, circle)
		ctx.beginPath();
		ctx.arc(x + 18, y - 14, 12, 0, 2 * Math.PI);
		ctx.fillStyle = '#fff';
		ctx.fill();
		ctx.stroke();
		// Beak (triangle)
		ctx.beginPath();
		ctx.moveTo(x + 30, y - 14);
		ctx.lineTo(x + 38, y - 11);
		ctx.lineTo(x + 30, y - 7);
		ctx.closePath();
		ctx.fillStyle = '#ffae42';
		ctx.fill();
		ctx.stroke();
		// Comb (red, 2 circles)
		ctx.beginPath();
		ctx.arc(x + 20, y - 24, 4, 0, 2 * Math.PI);
		ctx.arc(x + 26, y - 26, 3, 0, 2 * Math.PI);
		ctx.fillStyle = '#e74c3c';
		ctx.fill();
		// Legs (yellow, lines)
		ctx.strokeStyle = '#ffae42';
		ctx.lineWidth = 4;
		ctx.beginPath();
		ctx.moveTo(x - 8, y + 16);
		ctx.lineTo(x - 8, y + 28);
		ctx.moveTo(x + 8, y + 16);
		ctx.lineTo(x + 8, y + 28);
		ctx.stroke();
		// Police hat (navy, rectangle and ellipse)
		ctx.beginPath();
		ctx.ellipse(x + 18, y - 24, 12, 5, 0, 0, 2 * Math.PI);
		ctx.fillStyle = '#222b4f';
		ctx.fill();
		ctx.stroke();
		ctx.beginPath();
		ctx.rect(x + 8, y - 34, 20, 10);
		ctx.fillStyle = '#222b4f';
		ctx.fill();
		ctx.stroke();
		// Badge (yellow star)
		ctx.save();
		ctx.translate(x + 18, y - 28);
		ctx.rotate(Math.PI / 10);
		ctx.beginPath();
		for (let i = 0; i < 5; i++) {
			ctx.lineTo(0, 5);
			ctx.translate(0, 5);
			ctx.rotate((Math.PI * 2) / 5);
			ctx.lineTo(0, -5);
			ctx.translate(0, -5);
			ctx.rotate(-(Math.PI * 6) / 5);
		}
		ctx.closePath();
		ctx.fillStyle = '#FFD700';
		ctx.fill();
		ctx.restore();
		// Wing (blue, arc)
		ctx.beginPath();
		ctx.arc(x - 10, y, 10, Math.PI * 0.2, Math.PI * 1.2, false);
		ctx.lineWidth = 6;
		ctx.strokeStyle = '#1e90ff';
		ctx.stroke();
		ctx.restore();
	}

	function drawHorse(x, y) {
		// Lower the horse so its hooves touch the ground
		y = Math.max(y, 350 * 0.7 + 36); // 350 is canvas height, 0.7 is ground start
		// Body
		ctx.save();
		ctx.beginPath();
		ctx.ellipse(x, y, 34, 18, 0, 0, 2 * Math.PI);
		ctx.fillStyle = '#a0522d';
		ctx.fill();
		ctx.lineWidth = 4;
		ctx.strokeStyle = '#6e4b2a';
		ctx.stroke();
		// Head (more defined)
		ctx.beginPath();
		ctx.ellipse(x + 36, y - 12, 13, 10, 0, 0, 2 * Math.PI);
		ctx.fillStyle = '#a0522d';
		ctx.fill();
		ctx.stroke();
		// Ears
		ctx.beginPath();
		ctx.moveTo(x + 44, y - 22);
		ctx.lineTo(x + 47, y - 32);
		ctx.lineTo(x + 41, y - 20);
		ctx.closePath();
		ctx.fillStyle = '#6e4b2a';
		ctx.fill();
		ctx.beginPath();
		ctx.moveTo(x + 30, y - 22);
		ctx.lineTo(x + 27, y - 32);
		ctx.lineTo(x + 33, y - 20);
		ctx.closePath();
		ctx.fill();
		// Mane
		ctx.beginPath();
		ctx.moveTo(x + 28, y - 18);
		ctx.lineTo(x + 26, y - 28);
		ctx.lineTo(x + 32, y - 18);
		ctx.lineTo(x + 36, y - 28);
		ctx.lineTo(x + 38, y - 18);
		ctx.closePath();
		ctx.fillStyle = '#3e2723';
		ctx.fill();
		// Legs (touching ground)
		ctx.strokeStyle = '#8b4513';
		ctx.lineWidth = 5;
		ctx.beginPath();
		ctx.moveTo(x - 16, y + 18);
		ctx.lineTo(x - 16, 350 * 0.7 + 60);
		ctx.moveTo(x - 6, y + 18);
		ctx.lineTo(x - 6, 350 * 0.7 + 60);
		ctx.moveTo(x + 6, y + 18);
		ctx.lineTo(x + 6, 350 * 0.7 + 60);
		ctx.moveTo(x + 16, y + 18);
		ctx.lineTo(x + 16, 350 * 0.7 + 60);
		ctx.stroke();
		// Hooves
		ctx.fillStyle = '#222';
		ctx.fillRect(x - 19, 350 * 0.7 + 60, 6, 6);
		ctx.fillRect(x - 9, 350 * 0.7 + 60, 6, 6);
		ctx.fillRect(x + 3, 350 * 0.7 + 60, 6, 6);
		ctx.fillRect(x + 13, 350 * 0.7 + 60, 6, 6);
		// Tail (smaller)
		ctx.beginPath();
		ctx.moveTo(x - 32, y + 6);
		ctx.bezierCurveTo(x - 38, y + 18, x - 40, y + 28, x - 28, y + 28);
		ctx.strokeStyle = '#3e2723';
		ctx.lineWidth = 5;
		ctx.stroke();
		ctx.restore();
	}


	function drawOfficer(x, y) {
		// Legs
		ctx.strokeStyle = '#000';
		ctx.lineWidth = 3;
		ctx.beginPath();
		ctx.moveTo(x - 6, y + 28);
		ctx.lineTo(x - 6, y + 44);
		ctx.moveTo(x + 6, y + 28);
		ctx.lineTo(x + 6, y + 44);
		ctx.stroke();
		// Body
		ctx.beginPath();
		ctx.ellipse(x, y + 16, 12, 16, 0, 0, 2 * Math.PI);
		ctx.fillStyle = '#1e90ff';
		ctx.fill();
		// Head
		ctx.beginPath();
		ctx.arc(x, y, 10, 0, 2 * Math.PI);
		ctx.fillStyle = '#ffe0bd';
		ctx.fill();
		// Hat
		ctx.beginPath();
		ctx.ellipse(x, y - 10, 12, 4, 0, 0, 2 * Math.PI);
		ctx.fillStyle = '#222';
		ctx.fill();
		ctx.beginPath();
		ctx.rect(x - 8, y - 18, 16, 8);
		ctx.fillStyle = '#222';
		ctx.fill();
		// Badge
		ctx.beginPath();
		ctx.arc(x + 8, y + 16, 3, 0, 2 * Math.PI);
		ctx.fillStyle = '#FFD700';
		ctx.fill();
		// Arms
		ctx.strokeStyle = '#1e90ff';
		ctx.lineWidth = 3;
		ctx.beginPath();
		ctx.moveTo(x - 12, y + 16);
		ctx.lineTo(x - 24, y + 28);
		ctx.moveTo(x + 12, y + 16);
		ctx.lineTo(x + 24, y + 8);
		ctx.stroke();
	}

	function animate() {
		ctx.clearRect(0, 0, canvas.width, canvas.height);
		drawBackground();
		// Animate person running, horse, and sheriff hen
		drawPerson(personX, canvas.height * 0.75 + Math.sin(frame / 8) * 2);
		// Place horse so its hooves touch the ground
		const horseY = 350 * 0.7 + 18; // 350 is canvas height, 0.7 is ground start
		drawHorse(horseX, horseY);
		drawSheriffHen(horseX + 10, horseY - 38);

		// Move horse and person at the same pace, keep gap
		horseX += 1.2;
		personX = horseX + 120;
		if (horseX > canvas.width - 80) {
			horseX = 60;
			personX = horseX + 120;
		}

		frame++;
		requestAnimationFrame(animate);
	}

	animate();
};
