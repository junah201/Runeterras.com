import React from "react";
import styled from "styled-components";
import axios, { AxiosResponse } from "axios";
import { getDeckFromCode } from "lor-deckcodes-ts";
import { IDeckCompareDetailInfo } from "../types/deck";
import CompareDeck from "./../components/deck/CompareDeck";
import GameVersionSelector from "../components/common/GameVersionSelector";
import { IGameVersion } from "./../types/gameVersion";

const StyledAllMetaDeckComparePage = styled.main`
	margin: 60px 0;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
`;
const StyledAllMetaDeckCompareWrapper = styled.div``;

const StyledDeckList = styled.div`
	display: flex;
	flex-direction: column;

	align-items: center;
	justify-content: center;
`;

const AllMetaDeckComparePage: React.FC = () => {
	const [deckCompareDatas, setDeckCompareDatas] = React.useState<
		IDeckCompareDetailInfo[]
	>([]);

	const [gameVersion, setGameVersion] = React.useState<IGameVersion>();

	React.useEffect(() => {
		axios({
			url: `${process.env.REACT_APP_API_URL}/deck/compare/all`,
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				Accept: "application/json",
			},
			params: {
				skip: 0,
				limit: 20,
				game_version: gameVersion?.game_version,
			},
		}).then((res: AxiosResponse) => {
			if (res.status === 200) {
				setDeckCompareDatas(
					res.data.filter((_: any, i: number) => i % 2 === 0)
				);
			}
		});
	}, [gameVersion]);

	return (
		<StyledAllMetaDeckComparePage>
			<StyledAllMetaDeckCompareWrapper>
				<GameVersionSelector setGameVersion={setGameVersion} />
				<StyledDeckList>
					{deckCompareDatas.map((deckCompareData) => {
						return (
							<CompareDeck key={deckCompareData.id} data={deckCompareData} />
						);
					})}
				</StyledDeckList>
			</StyledAllMetaDeckCompareWrapper>
		</StyledAllMetaDeckComparePage>
	);
};

export default AllMetaDeckComparePage;
