import React from "react";
import styled from "styled-components";

import Deck from "../components/deck/Deck";
import { IDeckInfo } from "../types/deck";
import { IGameVersion } from "../types/gameVersion";

import axios, { AxiosResponse } from "axios";

import { getDeckFromCode } from "lor-deckcodes-ts";
import GameVersionSelector from "../components/common/GameVersionSelector";

import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";
import updateLocale from "dayjs/plugin/updateLocale";
dayjs.extend(relativeTime);
dayjs.extend(utc);
dayjs.extend(updateLocale);

dayjs.updateLocale("en", {
	relativeTime: {
		future: "in %s",
		past: "%s ago",
		s: "a few seconds",
		m: "a minute",
		mm: "%d minutes",
		h: "1 hour",
		hh: "%d hours",
		d: "1 day",
		dd: "%d days",
		M: "1 month",
		MM: "%d months",
		y: "1 year",
		yy: "%d years",
	},
});

const StyledMainPage = styled.main`
	margin: 60px 0;
`;

const StyledIntroductionContainer = styled.div`
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 20px;

	& h1 {
		color: #ffffff;
		font-size: 40px;
		font-weight: bold;
	}

	& p {
		color: #ffffff;
		font-size: 20px;
	}
`;

const StyledDeckContainer = styled.div`
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
`;

const StyledMoreDeckLink = styled.button`
	background-color: #262161;
	color: #ffffff;
	padding: 12px 0;
	width: min(1250px, 80vw);
	border-radius: 10px;
	font-size: 1rem;
	display: flex;
	align-items: center;
	justify-content: center;
	text-decoration: none;
	border: none;
`;

const StyledDeckListInfo = styled.div`
	width: min(1250px, 80vw);
	display: flex;
	flex-direction: row;
	align-items: center;
	justify-content: space-between;

	& p {
		font-size: 1rem;
		color: #ffffff;
	}
`;

const MetaDecksPage: React.FC = () => {
	const [gameVersion, setGameVersion] = React.useState<IGameVersion>();
	const [deckList, setDeckList] = React.useState<IDeckInfo[]>([]);

	const SIZE = 10;
	const [page, setPage] = React.useState(0);

	const fetch_deck_list = () => {
		axios({
			url: `${process.env.REACT_APP_API_URL}/deck/meta/all`,
			params: {
				limit: 10,
				skip: page,
				game_version: gameVersion?.game_version,
			},
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				Accept: "application/json",
			},
		}).then((res: AxiosResponse) => {
			if (res.status === 200) {
				const newDeckList: IDeckInfo[] = [];
				for (const deck of res.data) {
					const decodedDeck = getDeckFromCode(deck.deck_code);
					const newDeck: IDeckInfo = {
						id: deck.id,
						totalMatchCount: deck.win_count + deck.lose_count,
						winRate: (
							(deck.win_count * 100) /
							(deck.win_count + deck.lose_count)
						).toFixed(2),
						winCount: deck.win_count,
						loseCount: deck.lose_count,
						firstStartWinCount: deck.first_start_win_count,
						firstStartLoseCount: deck.first_start_lose_count,
						factions: [],
						champions: [],
						turns: deck.turns,
					};
					for (const card of decodedDeck) {
						newDeck.champions.push(card.cardCode);
					}
					newDeck.factions = [
						...new Set(
							decodedDeck.map((card) => `${card.cardCode.slice(2, 4)}`)
						),
					];
					newDeck.champions = decodedDeck.map((card) => card.cardCode);
					newDeckList.push(newDeck);
				}
				setDeckList((prev) => {
					return [...prev, ...newDeckList];
				});
			}
		});
	};

	React.useEffect(() => {
		setPage(0);
		setDeckList([]);
		fetch_deck_list();
	}, [gameVersion]);

	React.useEffect(() => {
		fetch_deck_list();
	}, [page]);

	return (
		<StyledMainPage>
			<StyledIntroductionContainer>
				<h1>Meta Decks</h1>
			</StyledIntroductionContainer>
			<StyledDeckContainer>
				<StyledDeckListInfo>
					<GameVersionSelector setGameVersion={setGameVersion} />
					<p>
						Last Updated :{" "}
						{!!gameVersion
							? dayjs.utc(gameVersion?.updated_at).fromNow()
							: "Loading..."}
					</p>
				</StyledDeckListInfo>
				{deckList.map((deck) => (
					<Deck key={`${deck.id}#${deck.totalMatchCount}`} deck={deck} />
				))}
				<StyledMoreDeckLink
					onClick={() => {
						setPage((prev) => prev + SIZE);
					}}
				>
					더 보기
				</StyledMoreDeckLink>
			</StyledDeckContainer>
		</StyledMainPage>
	);
};

export default MetaDecksPage;
