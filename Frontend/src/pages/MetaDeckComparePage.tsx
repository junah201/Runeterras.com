import React from "react";
import styled from "styled-components";
import axios from "axios";

import SelectDeck from "../components/deck/SelectDeck";
import { ChampionCard } from "../types/card";
import { IDeckCompareInfo } from "../types/deck";
import WinLosePieChart from "../components/chart/WinLosePieChart";
import TurnBarChart from "../components/chart/TurnBarChart";
import Card from "../components/card/Card";

const StyledMetaDeckComparePage = styled.main`
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	margin: 60px 0;
`;

const StyledMetaDeckCompareWrapper = styled.div`
	width: min(1250px, 80vw);
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
`;

const StyledSelectDeckButton = styled.button`
	padding: 10px 20px;
	border-radius: 2px;
	border: none;
	background-color: #534ac1;
	color: #ffffff;
	font-size: 1.5rem;
	font-weight: bold;
	margin: 1rem;
`;

const StyledDetailContainer = styled.div`
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

const MetaDeckComparePage: React.FC = () => {
	const [championCards, setChampionCards] = React.useState([]);
	const [firstDeckChampionCards, setFirstDeckChampionCards] = React.useState<
		ChampionCard[]
	>([]);
	const [secondDeckChampionCards, setSecondDeckChampionCards] = React.useState<
		ChampionCard[]
	>([]);

	const [metaDeckCompareData, setMetaDeckCompareData] =
		React.useState<IDeckCompareInfo | null>(null);

	React.useEffect(() => {
		axios({
			url: `${process.env.REACT_APP_API_URL}/card/champion/all`,
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				Accept: "application/json",
			},
		}).then((res) => {
			if (res.status === 200) {
				setChampionCards(res.data);
				console.log(res.data);
			}
		});
	}, []);

	React.useEffect(() => {
		setMetaDeckCompareData(null);
	}, [firstDeckChampionCards, secondDeckChampionCards]);

	return (
		<StyledMetaDeckComparePage>
			<StyledMetaDeckCompareWrapper>
				<SelectDeck
					deckChampionCards={firstDeckChampionCards}
					setDeckChampionCards={setFirstDeckChampionCards}
					championCards={championCards}
				/>
				<SelectDeck
					deckChampionCards={secondDeckChampionCards}
					setDeckChampionCards={setSecondDeckChampionCards}
					championCards={championCards}
				/>
				<StyledSelectDeckButton
					onClick={() => {
						if (firstDeckChampionCards.length === 0) {
							return alert("Please select A deck.");
						}

						if (secondDeckChampionCards.length === 0) {
							return alert("Please select B deck.");
						}

						setMetaDeckCompareData(null);
						axios({
							url: `${process.env.REACT_APP_API_URL}/deck/compare`,
							method: "GET",
							params: {
								my_deck_cards: firstDeckChampionCards
									.map((champion) => champion.id)
									.join(","),
								opponent_deck_cards: secondDeckChampionCards
									.map((champion) => champion.id)
									.join(","),
							},
							headers: {
								"Content-Type": "application/json",
								Accept: "application/json",
							},
						})
							.then((res) => {
								if (res.status !== 200) {
									setMetaDeckCompareData(null);
									if (res.status === 400) {
										return alert(res.data.message);
									}
									if (res.status === 404) {
										return alert(
											`해당 덱의 데이터를 찾을 수 없습니다. (${res.data.message})`
										);
									}
									return alert(
										`알 수 없는 오류가 발생했습니다. (${res.data.message})`
									);
								}

								setMetaDeckCompareData(res.data as IDeckCompareInfo);
							})
							.catch((err) => {
								console.log(err);
								if (err.response.status !== 200) {
									setMetaDeckCompareData(null);
									if (err.response.status === 400) {
										return alert(err.response.data.message);
									}
									if (err.response.status === 404) {
										return alert(
											`해당 덱의 데이터를 찾을 수 없습니다. (${err.response.data.message})`
										);
									}
									return alert(
										`알 수 없는 오류가 발생했습니다. (${err.response.data.message})`
									);
								}
							});
					}}
				>
					비교 결과 보기
				</StyledSelectDeckButton>
				{metaDeckCompareData && (
					<StyledDetailContainer>
						<h1>
							Result{" "}
							<small>
								(Total{" "}
								{metaDeckCompareData.win_count + metaDeckCompareData.lose_count}{" "}
								Matches)
							</small>
						</h1>
						<StyledDeckContainer>
							<StyledDecksInfoContainer>
								<StyledCardsContainer>
									{firstDeckChampionCards.map((card) => {
										return <Card key={card.id} id={card.id} />;
									})}
								</StyledCardsContainer>
								<StyledDeckInfoContainer>
									<p>{metaDeckCompareData.win_count} Win</p>
									<p>{metaDeckCompareData.lose_count} Lose</p>
								</StyledDeckInfoContainer>
							</StyledDecksInfoContainer>
							<span>VS</span>
							<StyledDecksInfoContainer>
								<StyledCardsContainer>
									{secondDeckChampionCards.map((card) => {
										return <Card key={card.id} id={card.id} />;
									})}
								</StyledCardsContainer>
								<StyledDeckInfoContainer>
									<p>{metaDeckCompareData.lose_count} Win</p>
									<p>{metaDeckCompareData.win_count} Lose</p>
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
										value: metaDeckCompareData.first_start_lose_count,
									},
									{
										id: "B 덱 선공",
										name: "B 덱 선공",
										value:
											metaDeckCompareData.lose_count -
											metaDeckCompareData.first_start_lose_count,
									},
									{
										id: "A 덱 후공",
										name: "A 덱 후공",
										value:
											metaDeckCompareData.win_count -
											metaDeckCompareData.first_start_win_count,
									},
									{
										id: "A 덱 선공",
										name: "A 덱 선공",
										value: metaDeckCompareData.first_start_win_count,
									},
								]}
							/>
							<WinLosePieChart
								title={"Lose"}
								data={[
									{
										id: "B 덱 후공",
										name: "B 덱 후공",
										value: metaDeckCompareData.first_start_win_count,
									},
									{
										id: "B 덱 선공",
										name: "B 덱 선공",
										value:
											metaDeckCompareData.win_count -
											metaDeckCompareData.first_start_win_count,
									},
									{
										id: "A 덱 후공",
										name: "A 덱 후공",
										value:
											metaDeckCompareData.lose_count -
											metaDeckCompareData.first_start_lose_count,
									},
									{
										id: "A 덱 선공",
										name: "A 덱 선공",
										value: metaDeckCompareData.first_start_lose_count,
									},
								]}
							/>
						</StyledDetailPieChartContainer>
						<StyledDetailPieChartContainer>
							<TurnBarChart
								data={Object.entries(metaDeckCompareData.turn).map(
									(item: any) => {
										return {
											turn: item[0],
											"A win": item[1].win,
											B_win: item[1].lose,
										};
									}
								)}
								keys={["A win", "B_win"]}
							/>
						</StyledDetailPieChartContainer>
					</StyledDetailContainer>
				)}
			</StyledMetaDeckCompareWrapper>
		</StyledMetaDeckComparePage>
	);
};

export default MetaDeckComparePage;
