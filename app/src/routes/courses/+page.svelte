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
</script>

{#if urlParams}
	<Svelecte
		multiple
		clearable
		placeholder="Select courses"
		options={Object.keys(data.catalogData[selectedCatalog]['courses'])}
		bind:value={selectedCourses}
	></Svelecte>
	<p>Selected courses:</p>
	<ul>
		{#each selectedCourses as course}
			<li>{course}</li>
		{/each}
	</ul>
	<button onclick={goToNext}> Next </button>
{/if}
