<script lang="ts">
	import { goto } from '$app/navigation';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();
	// svelte-ignore non_reactive_update
	let selectedCatalog = 'Fall 2025 Undergraduate';
	const catalogs = data.catalogs;

	function goToNext() {
		goto(`/courses?catalog=${encodeURIComponent(selectedCatalog)}`);
	}
</script>

<label for="catalogSelect">Select a semester:</label>
<select id="catalogSelect" bind:value={selectedCatalog}>
	{#each catalogs as catalog}
		<option value={catalog}>{catalog}</option>
	{/each}
</select>
<button onclick={goToNext}>Next</button>
