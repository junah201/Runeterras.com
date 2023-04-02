import React from "react";
import styled from "styled-components";
import queryString from "query-string";
import { useLocation, useHistory } from "react-router-dom";

import Deck from "../components/deck/Deck";
import { IDeckInfo } from "../types/deck";
import { IGameVersion } from "../types/gameVersion";

import axios, { AxiosResponse } from "axios";

import { getDeckFromCode } from "lor-deckcodes-ts";

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

const StyledGameVersionSelector = styled.select`
	background-color: #262161;
	font-size: 1rem;
	color: #ffffff;
	border: none;
	padding: 4px;
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
	const [allGameVersions, setAllGameVersions] = React.useState<IGameVersion[]>(
		[]
	);
	const [gameVersion, setGameVersion] = React.useState<string>("");
	const [lastUpdatedAt, setLastUpdatedAt] = React.useState("Loading...");
	const [deckList, setDeckList] = React.useState<IDeckInfo[]>([]);

	const SIZE = 10;
	const [page, setPage] = React.useState(0);

	React.useEffect(() => {
		axios({
			url: `${process.env.REACT_APP_API_URL}/game_version/all`,
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				Accept: "application/json",
			},
		}).then((res: AxiosResponse) => {
			if (res.status === 200) {
				const sortedGameVersions: IGameVersion[] = res.data.sort(
					(a: IGameVersion, b: IGameVersion) =>
						a.game_version < b.game_version ? 1 : -1
				);
				setGameVersion(sortedGameVersions[0].game_version);
				setLastUpdatedAt(dayjs.utc(sortedGameVersions[0].updated_at).fromNow());
				setAllGameVersions(sortedGameVersions);
			}
		});
	}, []);

	React.useEffect(() => {
		axios({
			url: `${process.env.REACT_APP_API_URL}/deck/meta/all`,
			params: {
				limit: 10,
				skip: page,
				game_version: gameVersion,
			},
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				Accept: "application/json",
			},
		}).then((res) => {
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
	}, [page, gameVersion]);

	return (
		<StyledMainPage>
			<StyledIntroductionContainer>
				<h1>Meta Decks</h1>
			</StyledIntroductionContainer>
			<StyledDeckContainer>
				<StyledDeckListInfo>
					<p>
						Version :{" "}
						<StyledGameVersionSelector
							onChange={(e) => {
								setGameVersion(e.target.value);
								const tmp = allGameVersions.find(
									(gameVersion) => gameVersion.game_version === e.target.value
								) as IGameVersion;
								setLastUpdatedAt(dayjs.utc(tmp.updated_at).fromNow());
								setDeckList([]);
								setPage(0);
							}}
						>
							{allGameVersions
								.sort((a, b) => (a.game_version < b.game_version ? 1 : -1))
								.map((gameVersion) => {
									return (
										<option
											key={gameVersion.game_version}
											value={gameVersion.game_version}
										>
											{gameVersion.game_version} (
											{gameVersion.total_match_count} Match)
										</option>
									);
								})}
						</StyledGameVersionSelector>
					</p>
					<p>Last Updated : {lastUpdatedAt}</p>
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
