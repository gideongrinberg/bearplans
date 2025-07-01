<script lang="ts">
	import { goto } from '$app/navigation';
	import Svelecte from 'svelecte';
	import { onMount } from 'svelte';

	const { data } = $props();
	let selectedCourses: string[] = $state([]);
	let urlParams: URLSearchParams | undefined = $state();
	let selectedCatalog = $derived(urlParams?.get('catalog') ?? 'Fall 2025 Undergraduate');
	onMount(() => {
		urlParams = new URLSearchParams(window.location.search);
	});

	function goToNext() {
		const courses = selectedCourses.map((v) => data.catalogData[selectedCatalog]['courses'][v]);
		goto(
			`/schedule?courses=${encodeURIComponent(JSON.stringify(courses))}&catalog=${encodeURIComponent(selectedCatalog)}`
		);
	}

	function goBack() {
		goto('/');
	}
</script>

{#if urlParams}
	<div class="page-card">
		<h1 class="page-title">Select Courses</h1>
		<p class="subtitle">Choose the courses you want to include in your schedule for <strong>{selectedCatalog}</strong>.</p>
		
		<div class="form-group">
			<label class="form-label">Available Courses:</label>
			<div class="svelecte-wrapper">
				<Svelecte
					multiple
					clearable
					placeholder="Search and select courses..."
					options={Object.keys(data.catalogData[selectedCatalog]['courses'])}
					bind:value={selectedCourses}
				></Svelecte>
			</div>
		</div>

		{#if selectedCourses.length > 0}
			<div class="selected-courses">
				<h3 class="selected-title">Selected courses ({selectedCourses.length}):</h3>
				<div class="course-grid">
					{#each selectedCourses as course}
						<div class="course-chip">
							{course}
							<button 
								class="remove-btn"
								onclick={() => {
									selectedCourses = selectedCourses.filter(c => c !== course);
								}}
								aria-label="Remove {course}"
							>
								×
							</button>
						</div>
					{/each}
				</div>
			</div>
		{/if}

		<div class="navigation">
			<button class="btn" onclick={goBack}>
				← Back
			</button>
			<div class="step-indicator">
				<span>Step 2 of 3</span>
			</div>
			<button 
				class="btn btn-primary" 
				onclick={goToNext}
				disabled={selectedCourses.length === 0}
			>
				View Schedules →
			</button>
		</div>
	</div>
{/if}

<style>
	.subtitle {
		text-align: center;
		color: #6b7280;
		margin-bottom: 2rem;
		font-size: 1.125rem;
	}

	.svelecte-wrapper {
		margin-bottom: 1.5rem;
	}

	.svelecte-wrapper :global(.svelecte) {
		border-radius: 8px;
		border: 1px solid #d1d5db;
		font-size: 1rem;
	}

	.svelecte-wrapper :global(.svelecte:focus-within) {
		border-color: #4f46e5;
		box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
	}

	.selected-courses {
		margin-bottom: 2rem;
	}

	.selected-title {
		font-size: 1.125rem;
		font-weight: 600;
		color: #374151;
		margin-bottom: 1rem;
	}

	.course-grid {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
	}

	.course-chip {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		background: #ede9fe;
		color: #5b21b6;
		padding: 0.5rem 0.75rem;
		border-radius: 6px;
		font-size: 0.875rem;
		font-weight: 500;
	}

	.remove-btn {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 18px;
		height: 18px;
		border: none;
		background: rgba(91, 33, 182, 0.2);
		color: #5b21b6;
		border-radius: 50%;
		cursor: pointer;
		font-size: 14px;
		line-height: 1;
		transition: background-color 0.2s ease;
	}

	.remove-btn:hover {
		background: rgba(91, 33, 182, 0.3);
	}

	.btn:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.btn:disabled:hover {
		transform: none;
		box-shadow: none;
	}
	
	@media (max-width: 768px) {
		.course-grid {
			gap: 0.375rem;
		}
		
		.course-chip {
			font-size: 0.8rem;
			padding: 0.375rem 0.5rem;
		}
		
		.remove-btn {
			width: 16px;
			height: 16px;
			font-size: 12px;
		}
	}
</style>
