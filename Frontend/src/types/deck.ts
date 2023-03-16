import { Card } from "./card";

export interface DeckInfo {
	id: number;
	pickRate: number;
	winRate: number;
	factions: string[];
	champions: string[];
	cards: Card[];
}
