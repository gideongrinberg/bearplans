<script>
	//@ts-nocheck
	let { schedule } = $props();

	const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
	const dayMap = {
		Mon: 0,
		Tue: 1,
		Wed: 2,
		Thu: 3,
		Fri: 4,
		Sat: 5,
		Sun: 6
	};

	// Find min and max times
	let minTime = 24 * 60;
	let maxTime = 0;

	schedule.forEach((section) => {
		minTime = Math.min(minTime, section.start);
		maxTime = Math.max(maxTime, section.end);
	});

	// Round to nearest hour for display
	minTime = Math.floor(minTime / 60) * 60;
	maxTime = Math.ceil(maxTime / 60) * 60;

	minTime = Math.min(minTime, 8 * 60);
	maxTime = Math.max(maxTime, 15 * 60);

	// Generate time labels
	const timeLabels = [];
	for (let t = minTime; t <= maxTime; t += 60) {
		const hour = Math.floor(t / 60);
		const displayHour = hour === 0 ? 12 : hour > 12 ? hour - 12 : hour;
		const ampm = hour < 12 ? 'AM' : 'PM';
		timeLabels.push({ time: t, label: `${displayHour}:00 ${ampm}` });
	}

	// Group sections by day
	const sectionsByDay = days.map(() => []);
	schedule.forEach((section) => {
		section.days.forEach((day) => {
			const dayIndex = dayMap[day];
			if (dayIndex !== undefined) {
				sectionsByDay[dayIndex].push(section);
			}
		});
	});

	function shouldHideInstructor(section) {
		const totalMinutes = maxTime - minTime;
		const heightPercent = ((section.end - section.start) / totalMinutes) * 100;
		const calendarHeight = 600;
		return Math.floor((heightPercent / 100) * calendarHeight) < 36;
	}

	// Calculate position and height for a section
	function getSectionStyle(section) {
		const totalMinutes = maxTime - minTime;
		const top = ((section.start - minTime) / totalMinutes) * 100;
		const height = ((section.end - section.start) / totalMinutes) * 100;
		return `top: ${top}%; height: ${height}%;`;
	}

	// Format time for display
	function formatTime(minutes) {
		const hour = Math.floor(minutes / 60);
		const min = minutes % 60;
		const displayHour = hour === 0 ? 12 : hour > 12 ? hour - 12 : hour;
		const ampm = hour < 12 ? 'AM' : 'PM';
		return `${displayHour}:${min.toString().padStart(2, '0')} ${ampm}`;
	}

	function getColor(index) {
		const colors = [
			'#BA0C2F',
			'#215732',
			'#007D8A',
			'#F1B434',
			'#FF6D6A',
			'#971B2F',
			'#13322B',
			'#B5E3D8'
		];
		return colors[index % colors.length];
	}
</script>

<div class="schedule-container">
	<div class="header">
		<div class="time-header"></div>
		{#each days as day}
			<div class="day-header">{day}</div>
		{/each}
	</div>

	<div class="calendar-body">
		<div class="time-column">
			{#each timeLabels as { label }}
				<div class="time-label">{label}</div>
			{/each}
		</div>

		<div class="days-container">
			{#each sectionsByDay as sections, dayIndex}
				<div class="day-column">
					<div class="sections-container">
						{#each sections as section, i}
							<div
								class="section"
								style="{getSectionStyle(section)} background-color: {getColor(i)};"
								title="{section.id} ({formatTime(section.start)} - {formatTime(section.end)}){section.instructor ? `, taught by ${section.instructor}` : ''}"
							>
								<div class="section-time">
									{formatTime(section.start)} - {formatTime(section.end)}
								</div>
								<div class="section-instructor">{section.id}</div>
								{#if section.instructor && !shouldHideInstructor(section)}
									<div class="section-instructor">{section.instructor}</div>
								{/if}
							</div>
						{/each}
					</div>
				</div>
			{/each}
		</div>
	</div>
</div>

<style>
	.schedule-container {
		font-family:
			-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
		background: white;
		border-radius: 12px;
		box-shadow:
			0 20px 25px -5px rgba(0, 0, 0, 0.1),
			0 10px 10px -5px rgba(0, 0, 0, 0.04);
		overflow: hidden;
	}

	.header {
		display: grid;
		grid-template-columns: 80px repeat(7, 1fr);
		background: #f9fafb;
		border-bottom: 1px solid #e5e7eb;
	}

	.time-header {
		border-right: 1px solid #e5e7eb;
	}

	.day-header {
		padding: 12px;
		text-align: center;
		font-weight: 600;
		color: var(--washu-black);
		border-right: 1px solid #e5e7eb;
	}

	.day-header:last-child {
		border-right: none;
	}

	.calendar-body {
		display: grid;
		grid-template-columns: 80px 1fr;
		min-height: 600px;
	}

	.time-column {
		border-right: 1px solid #e5e7eb;
		position: relative;
	}

	.time-label {
		position: absolute;
		right: 8px;
		font-size: 12px;
		color: #6b7280;
		transform: translateY(-50%);
		font-weight: 500;
	}

	.time-label:nth-child(1) {
		top: 0%;
	}
	.time-label:nth-child(2) {
		top: calc(100% / (var(--time-slots, 8) - 1));
	}
	.time-label:nth-child(3) {
		top: calc(200% / (var(--time-slots, 8) - 1));
	}
	.time-label:nth-child(4) {
		top: calc(300% / (var(--time-slots, 8) - 1));
	}
	.time-label:nth-child(5) {
		top: calc(400% / (var(--time-slots, 8) - 1));
	}
	.time-label:nth-child(6) {
		top: calc(500% / (var(--time-slots, 8) - 1));
	}
	.time-label:nth-child(7) {
		top: calc(600% / (var(--time-slots, 8) - 1));
	}
	.time-label:nth-child(8) {
		top: calc(700% / (var(--time-slots, 8) - 1));
	}
	.time-label:nth-child(n + 9) {
		top: 100%;
	}

	.days-container {
		display: grid;
		grid-template-columns: repeat(7, 1fr);
		position: relative;
	}

	.day-column {
		border-right: 1px solid #e5e7eb;
		position: relative;
	}

	.day-column:last-child {
		border-right: none;
	}

	.sections-container {
		position: absolute;
		inset: 0;
		padding: 0 4px;
	}

	.section {
		position: absolute;
		left: 4px;
		right: 4px;
		border-radius: 4px;
		padding: 4px 8px;
		color: white;
		font-size: 13px;
		overflow: hidden;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.section-time {
		font-weight: 500;
		font-size: 11px;
		margin: 0px;
		line-height: 1;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.section-instructor {
		font-size: 11px;
		opacity: 0.9;
		margin: 0px;
		line-height: 1;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	@media (max-width: 768px) {
		.header {
			grid-template-columns: 60px repeat(7, 1fr);
		}

		.calendar-body {
			grid-template-columns: 60px 1fr;
		}

		.day-header {
			padding: 8px 4px;
			font-size: 12px;
		}

		.time-label {
			font-size: 10px;
			right: 4px;
		}

		.section {
			padding: 2px 4px;
			font-size: 11px;
		}

		.section-time {
			font-size: 10px;
		}

		.section-instructor {
			font-size: 9px;
		}
	}

	@media (max-width: 480px) {
		.schedule-container {
			border-radius: 8px;
		}

		.header {
			grid-template-columns: 50px repeat(7, 1fr);
		}

		.calendar-body {
			grid-template-columns: 50px 1fr;
			min-height: 400px;
		}

		.day-header {
			padding: 6px 2px;
			font-size: 10px;
		}

		.time-label {
			font-size: 9px;
		}

		.section {
			padding: 1px 2px;
			font-size: 9px;
		}

		.section-time {
			font-size: 8px;
		}

		.section-instructor {
			font-size: 8px;
			margin-top: 1px;
		}
	}
</style>
