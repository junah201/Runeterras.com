import React from "react";
import styled from "styled-components";

import { IDeckCompareDetailInfo } from "../../types/deck";
import { Deck } from "lor-deckcodes-ts";
import Card from "../card/Card";
import WinLosePieChart from "../chart/WinLosePieChart";
import TurnBarChart from "../chart/TurnBarChart";

const StyledCompareDetail = styled.div`
	display: flex;
	flex-direction: column;
	width: min(1250px, 80vw);
	background-color: #262161;
	padding: 30px;

	& h1 {
		font-size: 2rem;
		font-weight: bold;
		color: #ffffff;

		& small {
			font-size: 1.5rem;
		}
	}
`;

const StyledCardsContainer = styled.div`
	display: flex;
	flex-direction: crow;
	align-items: center;
	justify-content: center;
	width: 315px;
`;

const StyledDetailPieChartContainer = styled.div`
	display: flex;
	flex-direction: row;
	justify-content: center;
	align-items: center;
	width: 100%;
	height: 400px;
`;

const StyledDecksInfoContainer = styled.div`
	display: flex;
	flex-direction: row;
	justify-content: space-around;
`;

const StyledDeckInfoContainer = styled.div`
	display: flex;
	flex-direction: column;
	padding: 60px 0;
	color: #ffffff;
`;

const StyledDeckContainer = styled.div`
	display: flex;
	flex-direction: column;
	justify-content: space-around;
	width: 100%;
	padding: 60px 0;

	& > span {
		width: 100%;
		text-align: center;
		font-size: 3rem;
		font-weight: bold;
		color: #ffffff;
	}
`;

const CompareDetail: React.FC<{
	data: IDeckCompareDetailInfo;
	myDeck: Deck;
	opponentDeck: Deck;
}> = ({ data, myDeck, opponentDeck }) => {
	return (
		<StyledCompareDetail>
			<h1>
				Result <small>(Total {data.win_count + data.lose_count} Matches)</small>
			</h1>
			<StyledDeckContainer>
				<StyledDecksInfoContainer>
					<StyledCardsContainer>
						{myDeck.map((card) => {
							return <Card key={card.cardCode} id={card.cardCode} />;
						})}
					</StyledCardsContainer>
					<StyledDeckInfoContainer>
						<p>{data.win_count} Win</p>
						<p>{data.lose_count} Lose</p>
					</StyledDeckInfoContainer>
				</StyledDecksInfoContainer>
				<span>VS</span>
				<StyledDecksInfoContainer>
					<StyledCardsContainer>
						{opponentDeck.map((card) => {
							return <Card key={card.cardCode} id={card.cardCode} />;
						})}
					</StyledCardsContainer>
					<StyledDeckInfoContainer>
						<p>{data.lose_count} Win</p>
						<p>{data.win_count} Lose</p>
					</StyledDeckInfoContainer>
				</StyledDecksInfoContainer>
			</StyledDeckContainer>
			<StyledDetailPieChartContainer>
				<WinLosePieChart
					title={"Win"}
					data={[
						{
							id: "B 덱 후공",
							name: "B 덱 후공",
							value: data.first_start_lose_count,
						},
						{
							id: "B 덱 선공",
							name: "B 덱 선공",
							value: data.lose_count - data.first_start_lose_count,
						},
						{
							id: "A 덱 후공",
							name: "A 덱 후공",
							value: data.win_count - data.first_start_win_count,
						},
						{
							id: "A 덱 선공",
							name: "A 덱 선공",
							value: data.first_start_win_count,
						},
					]}
					total={data.win_count + data.lose_count}
				/>
				<WinLosePieChart
					title={"Lose"}
					data={[
						{
							id: "B 덱 후공",
							name: "B 덱 후공",
							value: data.first_start_win_count,
						},
						{
							id: "B 덱 선공",
							name: "B 덱 선공",
							value: data.win_count - data.first_start_win_count,
						},
						{
							id: "A 덱 후공",
							name: "A 덱 후공",
							value: data.lose_count - data.first_start_lose_count,
						},
						{
							id: "A 덱 선공",
							name: "A 덱 선공",
							value: data.first_start_lose_count,
						},
					]}
					total={data.win_count + data.lose_count}
				/>
			</StyledDetailPieChartContainer>
			<StyledDetailPieChartContainer>
				<TurnBarChart
					data={Object.entries(data.turns).map((item: any) => {
						return {
							turn: item[0],
							"A win": item[1].W,
							"B win": item[1].L,
						};
					})}
					keys={["A win", "B win"]}
				/>
			</StyledDetailPieChartContainer>
		</StyledCompareDetail>
	);
};

export default CompareDetail;
