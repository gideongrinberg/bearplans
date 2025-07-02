<script lang="ts">
	import type { Catalog, Section } from '$lib/catalog';
	import { getValidSchedules } from '$lib/schedule';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import Schedule from './Schedule.svelte';

	let { data } = $props();
	let selectedCatalog: string = $state('');
	let selectedCourses: string[] = $state([]);
	let currentScheduleIndex = $state(0);

	onMount(() => {
		let urlParams = new URLSearchParams(window.location.search);
		selectedCatalog = urlParams.get('catalog') ?? 'Fall 2025';
		selectedCourses = JSON.parse(urlParams.get('courses') ?? '[]');
	});

	const getSchedules = async (courses: string[]): Promise<Section[][]> => {
		let catalog = data.catalogData[selectedCatalog];
		return new Promise((resolve, reject) => {
			resolve(getValidSchedules(courses, catalog));
		});
	};

	function goBack() {
		goto(`/courses?catalog=${encodeURIComponent(selectedCatalog)}`);
	}

	function nextSchedule(totalSchedules: number) {
		currentScheduleIndex = (currentScheduleIndex + 1) % totalSchedules;
	}

	function prevSchedule(totalSchedules: number) {
		currentScheduleIndex = (currentScheduleIndex - 1 + totalSchedules) % totalSchedules;
	}
</script>

{#if selectedCourses.length > 0}
	<div class="schedule-page">
		<div class="schedule-header">
			<h1 class="page-title">Your Schedule Options</h1>
			<p class="subtitle">Here are all possible schedules for your selected courses.</p>
		</div>

		{#await getSchedules(selectedCourses)}
			<div class="page-card">
				<div class="loading">
					<div class="loading-spinner"></div>
					<p>Generating your schedules...</p>
				</div>
			</div>
		{:then schedules}
			{#if schedules.length > 0}
				<div class="schedule-controls">
					{#if schedules.length > 1}
						<button class="btn" onclick={() => prevSchedule(schedules.length)}> ← Previous </button>
					{/if}

					<div class="schedule-info">
						<span class="schedule-counter">
							Schedule {currentScheduleIndex + 1} of {schedules.length}
						</span>
					</div>

					{#if schedules.length > 1}
						<button class="btn" onclick={() => nextSchedule(schedules.length)}> Next → </button>
					{/if}
				</div>

				<div class="schedule-wrapper">
					{#key currentScheduleIndex}
						<Schedule schedule={schedules[currentScheduleIndex]}></Schedule>
					{/key}
				</div>
			{:else}
				<div class="page-card">
					<div class="no-schedules">
						<h3>No Valid Schedules Found</h3>
						<p>
							Unfortunately, there are no valid schedules possible with your selected courses due to
							time conflicts.
						</p>
						<p>Try removing some courses or selecting different sections.</p>
					</div>
				</div>
			{/if}
		{/await}

		<div class="navigation">
			<button class="btn" onclick={goBack}> ← Back to Courses </button>
			<div class="step-indicator">
				<span>Step 3 of 3</span>
			</div>
			<div></div>
		</div>
	</div>
{:else}
	<div class="page-card">
		<div class="no-courses">
			<h3>No Courses Selected</h3>
			<p>Please go back and select some courses to generate schedules.</p>
			<button class="btn btn-primary" onclick={goBack}> Select Courses </button>
		</div>
	</div>
{/if}

<style>
	.schedule-page {
		width: 100%;
		max-width: 1400px;
		margin: 0 auto;
	}

	.schedule-header {
		text-align: center;
		margin-bottom: 2rem;
		color: white;
	}

	.schedule-header .page-title {
		font-family: var(--font-heading);
		color: var(--washu-white);
		text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
		margin-bottom: 0.5rem;
	}

	.subtitle {
		color: rgba(255, 255, 255, 0.9);
		font-size: 1.125rem;
		font-weight: 300;
		margin: 0;
	}

	.schedule-controls {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 1.5rem;
		background: white;
		padding: 1rem 1.5rem;
		border-radius: 12px;
		box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
	}

	.schedule-info {
		font-weight: 500;
		color: var(--washu-black);
	}

	.schedule-counter {
		font-size: 1.125rem;
	}

	.schedule-wrapper {
		margin-bottom: 2rem;
	}

	.loading {
		text-align: center;
		padding: 3rem 2rem;
	}

	.loading-spinner {
		width: 40px;
		height: 40px;
		border: 4px solid var(--washu-gray);
		border-top: 4px solid var(--washu-red);
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin: 0 auto 1rem;
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}

	.no-schedules,
	.no-courses {
		text-align: center;
		padding: 2rem;
	}

	.no-schedules h3,
	.no-courses h3 {
		font-family: var(--font-heading);
		color: var(--washu-red);
		margin-bottom: 1rem;
	}

	.no-schedules p,
	.no-courses p {
		color: #6b7280;
		margin-bottom: 1rem;
	}

	.navigation {
		background: white;
		padding: 1rem 1.5rem;
		border-radius: 12px;
		box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
	}

	@media (max-width: 768px) {
		.schedule-controls {
			flex-direction: column;
			gap: 1rem;
			text-align: center;
		}

		.schedule-controls .btn {
			width: 100%;
		}

		.schedule-info {
			order: -1;
		}
	}

	@media (max-width: 480px) {
		.schedule-header .page-title {
			font-size: 1.5rem;
		}

		.schedule-controls {
			padding: 1rem;
		}

		.navigation {
			padding: 1rem;
		}
	}
</style>
