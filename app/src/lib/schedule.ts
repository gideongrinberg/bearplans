import type { Catalog, Section } from './catalog';

function product<T>(arrays: T[][]): T[][] {
	return arrays.reduce<T[][]>((acc, curr) => acc.flatMap((a) => curr.map((b) => [...a, b])), [
		[]
	] as T[][]);
}

function combinations<T>(arr: T[], k: number): T[][] {
	if (k === 0) return [[]];
	if (arr.length < k) return [];
	const [head, ...tail] = arr;
	const withHead = combinations(tail, k - 1).map((comb) => [head, ...comb]);
	const withoutHead = combinations(tail, k);
	return [...withHead, ...withoutHead];
}

function overlaps(s1: Section, s2: Section) {
	for (const d1 of s1['days']) {
		for (const d2 of s2['days']) {
			if (d1 == d2) {
				if (s1.start < s2.end && s2.start < s1.end) {
					return true;
				}
			}
		}
	}

	return false;
}

export function getValidSchedules(courses: string[], catalog: Catalog) {
	const allSections: Section[][] = courses.map((v) => {
		const sections = catalog['sections'][v];
		if (!sections) throw new Error(`Unknown course ${v}`);
		return sections;
	});

	const asFlat = allSections.flat(1);

	const conflicts: Record<string, Set<string>> = {};
	for (const s1 of asFlat) {
		conflicts[s1['id']] = new Set();
		for (const s2 of asFlat) {
			if (s1['id'] == s2['id']) continue;
			if (overlaps(s1, s2)) {
				conflicts[s1['id']].add(s2['id']);
			}
		}
	}

	const validSchedules: Section[][] = [];
	for (const schedule of product(allSections)) {
		let valid = true;
		for (const [s1, s2] of combinations(schedule, 2)) {
			if (conflicts[s1.id].has(s2.id)) {
				valid = false;
				break;
			}
		}

		if (valid) {
			validSchedules.push(schedule);
		}
	}

	return validSchedules;
}
