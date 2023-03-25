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
	win: number;
	lose: number;
}
