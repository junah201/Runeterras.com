import React from "react";
import styled from "styled-components";
import { IGameVersion } from "../../types/gameVersion";

import axios, { AxiosResponse } from "axios";

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

const StyledGameVersionSelector = styled.p`
	color: #ffffff;

	& select {
		background-color: #262161;
		font-size: 1rem;
		color: #ffffff;
		border: none;
		padding: 4px;
	}
`;

const GameVersionSelector: React.FC<{
	setGameVersion: React.Dispatch<
		React.SetStateAction<IGameVersion | undefined>
	>;
}> = ({ setGameVersion }) => {
	const [allGameVersions, setAllGameVersions] = React.useState<IGameVersion[]>(
		[]
	);

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
				setGameVersion(sortedGameVersions[0]);
				setAllGameVersions(sortedGameVersions);
			}
		});
	}, [setGameVersion]);

	return (
		<StyledGameVersionSelector>
			Version :{" "}
			<select
				onChange={(e) => {
					for (const gameVersion of allGameVersions) {
						if (gameVersion.game_version === e.target.value) {
							setGameVersion(gameVersion);
							return;
						}
					}
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
								{gameVersion.game_version} ({gameVersion.total_match_count}{" "}
								Match)
							</option>
						);
					})}
			</select>
		</StyledGameVersionSelector>
	);
};

export default GameVersionSelector;
