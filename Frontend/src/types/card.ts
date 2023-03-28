export interface Card {
	id: number;
	name: string;
	filename: string;
}

export interface ChampionCard {
	id: string;
	is_champion: boolean;
	name: string;
	region: string;
	set: string;
	type: string;
}
