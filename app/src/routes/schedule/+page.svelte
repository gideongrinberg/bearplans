<script lang="ts">
	import type { Catalog, Section } from '$lib/catalog';
	import { getValidSchedules } from '$lib/schedule';
	import { onMount } from 'svelte';
	import Schedule from './Schedule.svelte';

	let { data } = $props();
	let selectedCatalog: string = $state('');
	let selectedCourses: string[] = $state([]);
	onMount(() => {
		let urlParams = new URLSearchParams(window.location.search);
		selectedCatalog = urlParams.get('catalog') ?? 'Fall 2025 Undergraduate';
		selectedCourses = JSON.parse(urlParams.get('courses') ?? '[]');
	});

	const getSchedules = async (courses: string[]) => {
		let catalog = data.catalogData[selectedCatalog];
		return new Promise((resolve, reject) => {
			resolve(getValidSchedules(courses, catalog));
		});
	};

	const getDate = (weekday: string, time: number) => {
		const days: Record<string, number> = {
			Sun: 0,
			Mon: 1,
			Tue: 2,
			Wed: 3,
			Thu: 4,
			Fri: 5,
			Sat: 6
		};

		const today = new Date();
		const todayDay = today.getDay();
		const targetDay = days[weekday];
		const delta = (targetDay - todayDay + 7) % 7 || 7;

		const date = new Date();
		date.setDate(date.getDate() + delta);
		date.setHours(0, 0, 0, 0);
		date.setMinutes(time);

		return date;
	};
</script>

{#if selectedCourses.length > 0}
	{#await getSchedules(selectedCourses)}
		<p>Getting schedules, please wait...</p>
	{:then schedules}
		<Schedule schedule={schedules[0]}></Schedule>
		<!-- <pre>
			{JSON.stringify(schedules, null, 4)}
        </pre> -->
	{/await}
{/if}
