export interface IDeckInfo {
	id: number;
	totalMatchCount: number;
	winCount: number;
	loseCount: number;
	firstStartWinCount: number;
	firstStartLoseCount: number;
	winRate: number | string;
	factions: string[];
	champions: string[];
	turns: { [key: string]: ITurnDetailInfo };
}

export interface IDeckDetailInfo {
	id: number;
	deck_code: IDeckCodeDetailInfo[];
	turn: { [key: string]: ITurnDetailInfo };
}

export interface IDeckCodeDetailInfo {
	deck_code: string;
	win: number;
	lose: number;
}

export interface ITurnDetailInfo {
	W: number;
	L: number;
}

export interface IDeckCompareInfo {
	id: number;
	my_deck_id: number;
	opponent_deck_id: number;
	win_count: number;
	lose_count: number;
	first_start_win_count: number;
	first_start_lose_count: number;
	turn: { [key: string]: ITurnDetailInfo };
}
