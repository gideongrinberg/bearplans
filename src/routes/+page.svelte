<script lang="ts">
	import { goto } from '$app/navigation';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();
	// svelte-ignore non_reactive_update
	let selectedCatalog = 'Fall 2025';
	const catalogs = data.catalogs;

	function goToNext() {
		goto(`/courses?catalog=${encodeURIComponent(selectedCatalog)}`);
	}
</script>

<div class="page-card">
	<h1 class="page-title">Course Scheduler</h1>
	<p class="subtitle">Select your semester to get started planning your schedule.</p>
	
	<div class="form-group">
		<label for="catalogSelect" class="form-label">Select a semester:</label>
		<select id="catalogSelect" class="form-select" bind:value={selectedCatalog}>
			{#each catalogs as catalog}
				<option value={catalog}>{catalog}</option>
			{/each}
		</select>
	</div>
	
	<div class="navigation">
		<div class="step-indicator">
			<span>Step 1 of 3</span>
		</div>
		<button class="btn btn-primary" onclick={goToNext}>
			Select Courses →
		</button>
	</div>
</div>

<style>
	.subtitle {
		text-align: center;
		color: #6b7280;
		margin-bottom: 2rem;
		font-size: 1.125rem;
	}
</style>
