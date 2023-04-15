import React from "react";
import styled from "styled-components";

import { IDeckInfo, IDeckDetailInfo } from "../../types/deck";
import axios from "axios";
import WinLosePieChart from "../chart/WinLosePieChart";
import TurnBarChart from "../chart/TurnBarChart";
import DeckCode from "./DeckCode";
import Card from "../card/Card";

const StyledDeck = styled.div`
	display: flex;
	flex-direction: column;
	align-items: center;
	background-color: #262161;
	border-radius: 10px;

	width: min(1250px, 80vw);
	margin: 12px 0;
	overflow: hidden;

	& > div + div {
		margin-top: 30px;
	}
`;

const StyledDeckPreview = styled.div`
	display: flex;
	flex-direction: row;
	align-items: center;
	justify-content: space-evenly;
	width: min(1250px, 80vw);
	height: 200px;
`;

const StyledDeckInfoContainer = styled.div`
	display: flex;
	flex-direction: column;
`;

const StyledDeckInfoWrapper = styled.div`
	display: flex;

	& + & {
		margin-top: 20px;
	}
`;

const StyledDeckRateInfo = styled.div`
	display: flex;
	flex-direction: column;

	color: #ffffff;

	& span {
		font-size: 1rem;
	}

	& span + span {
		margin-top: 8px;
	}
`;

const StyledFactionContainer = styled.div`
	display: flex;
	flex-direction: column;

	& div {
		height: 32px;
		width: 32px;

		& img {
			height: 100%;
			width: 100%;
			object-fit: cover;
		}
	}

	& div + div {
		margin-top: 24px;
	}
`;

const StyledDeckDivider = styled.div`
	width: 1px;
	height: 180px;
	margin: 0 5px;
	background-color: #534ac1;
`;

const StyledCardsContainer = styled.div`
	display: flex;
	flex-direction: row;
	align-items: center;
	justify-content: center;
`;

const StyledDetailButton = styled.button`
	width: 30px;
	height: 30px;
	border: none;
	background-color: #262161;
	margin: 0 30px;

	& img {
		height: 100%;
		width: 100%;
		object-fit: cover;
		filter: invert(78%) sepia(96%) saturate(1878%) hue-rotate(323deg)
			brightness(96%) contrast(99%);
	}
`;

const StyledDetailContainer = styled.div`
	display: flex;
	flex-direction: column;
	width: min(1250px, 80vw);
	background-color: #262161;
	padding: 30px;
`;

const StyledDetailPieChartContainer = styled.div`
	display: flex;
	flex-direction: row;
	justify-content: center;
	align-items: center;
	width: 100%;
	height: 400px;
`;

const StyledDetailDeckCodeContainer = styled.div`
	display: flex;
	flex-direction: column;
`;

const Deck: React.FC<{ deck: IDeckInfo }> = (props) => {
	const [isDetailOpen, setIsDetailOpen] = React.useState(false);
	const [detailInfo, setDetailInfo] = React.useState<IDeckDetailInfo | null>(
		null
	);

	const deckRef = React.useRef<HTMLDivElement>(null);

	React.useEffect(() => {
		if (!isDetailOpen) {
			return;
		}

		axios({
			url: `${process.env.REACT_APP_API_URL}/deck/meta/${props.deck.id}/detail`,
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				Accept: "application/json",
			},
		}).then((res) => {
			if (res.status === 200) {
				setDetailInfo(res.data);
			}
		});
	}, [isDetailOpen, props.deck.id]);

	return (
		<StyledDeck ref={deckRef} key={props.deck.id}>
			<StyledDeckPreview>
				<StyledDeckInfoContainer>
					<StyledDeckInfoWrapper>
						<StyledFactionContainer>
							{props.deck.factions.map((faction) => {
								return (
									<div>
										<img
											src={`${process.env.REACT_APP_CDN_URL}/images/faction/${faction}.svg`}
											alt={faction}
										/>
									</div>
								);
							})}
						</StyledFactionContainer>
					</StyledDeckInfoWrapper>
				</StyledDeckInfoContainer>
				<StyledDeckDivider />
				<StyledCardsContainer>
					{props.deck.champions.map((champion) => {
						return <Card id={champion} key={champion} />;
					})}
				</StyledCardsContainer>
				<StyledDeckDivider />
				<StyledDeckInfoWrapper>
					<StyledDeckRateInfo>
						<span>Total {props.deck.totalMatchCount} Matches</span>
						<span>
							Win Rate : {props.deck.winRate}% ({props.deck.winCount}W{" "}
							{props.deck.loseCount}L)
						</span>
					</StyledDeckRateInfo>
				</StyledDeckInfoWrapper>
				<StyledDetailButton
					onClick={(e) => {
						setIsDetailOpen((prev) => {
							if (!prev) {
								deckRef.current?.scrollIntoView({
									block: "start",
									behavior: "smooth",
								});
							}
							return !prev;
						});
					}}
				>
					<img src="/arrow_down.svg" alt="arrow_down" />
				</StyledDetailButton>
			</StyledDeckPreview>
			{isDetailOpen && (
				<StyledDetailContainer>
					<StyledDetailPieChartContainer>
						<WinLosePieChart
							title={"Win"}
							data={[
								{
									id: "후공",
									name: "후공",
									value: props.deck.winCount - props.deck.firstStartWinCount,
								},
								{
									id: "선공",
									name: "선공",
									value: props.deck.firstStartWinCount,
								},
							]}
							total={props.deck.winCount}
						/>
						<WinLosePieChart
							title={"Lose"}
							data={[
								{
									id: "후공",
									name: "후공",
									value: props.deck.loseCount - props.deck.firstStartLoseCount,
								},
								{
									id: "선공",
									name: "선공",
									value: props.deck.firstStartLoseCount,
								},
							]}
							total={props.deck.loseCount}
						/>
					</StyledDetailPieChartContainer>
					<StyledDetailPieChartContainer>
						{
							<TurnBarChart
								data={Object.entries(props.deck.turns).map((item: any, idx) => {
									return {
										turn: item[0],
										win: item[1].W,
										lose: item[1].L,
									};
								})}
								keys={["win", "lose"]}
							/>
						}
					</StyledDetailPieChartContainer>
					<StyledDetailDeckCodeContainer>
						{detailInfo &&
							detailInfo.deck_code
								.slice(0, 3)
								.map((item) => (
									<DeckCode
										key={item?.deck_code}
										code={item?.deck_code || ""}
										win_count={item?.win}
										lose_count={item?.lose}
									/>
								))}
					</StyledDetailDeckCodeContainer>
				</StyledDetailContainer>
			)}
		</StyledDeck>
	);
};

export default Deck;
