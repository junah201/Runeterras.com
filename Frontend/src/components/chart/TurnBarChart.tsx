import React from "react";
import { ResponsiveBar } from "@nivo/bar";
import styled from "styled-components";
import { ITurnDetailInfo } from "../../types/deck";

const StyledTurnBarChart = styled.div`
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	width: 100%;
	height: 100%;

	& span {
		font-size: 20px;
		font-weight: bold;
		color: #ffffff;
	}

	& text {
		color: #ffffff;
		fill: #ffffff;
	}
`;

const TurnBarChart: React.FC<{ data: { [key: string]: ITurnDetailInfo } }> = (
	props
) => {
	console.log(props.data);

	return (
		<StyledTurnBarChart>
			<span>Turn</span>
			<ResponsiveBar
				data={Object.entries(props.data).map((item: any) => {
					return {
						turn: item[0],
						win: item[1].win,
						lose: item[1].lose,
					};
				})}
				theme={{
					axis: {
						legend: {
							text: { fill: "#ffffff" },
						},
						ticks: {
							line: {
								stroke: "#ffffff",
							},
							text: {
								fill: "#ffffff",
							},
						},
					},
				}}
				keys={["lose", "win"]}
				indexBy="turn"
				margin={{ top: 50, right: 130, bottom: 80, left: 60 }}
				padding={0.3}
				valueScale={{ type: "linear" }}
				indexScale={{ type: "band", round: true }}
				colors={{ scheme: "nivo" }}
				borderColor={{
					from: "color",
					modifiers: [["darker", 1.6]],
				}}
				axisTop={null}
				axisRight={null}
				axisBottom={{
					tickSize: 5,
					tickPadding: 5,
					tickRotation: 0,
					legend: "win",
					legendPosition: "middle",
					legendOffset: 32,
				}}
				animate={false}
				axisLeft={{
					tickSize: 5,
					tickPadding: 5,
					tickRotation: 0,
					legend: "count",
					legendPosition: "middle",
					legendOffset: -40,
				}}
				labelSkipWidth={12}
				labelSkipHeight={12}
				labelTextColor="#ffffff"
				legends={[
					{
						dataFrom: "keys",
						anchor: "right",
						direction: "column",
						justify: false,
						translateX: 120,
						translateY: 0,
						itemsSpacing: 2,
						itemWidth: 100,
						itemHeight: 20,
						itemDirection: "left-to-right",
						itemOpacity: 0.85,
						symbolSize: 20,
						effects: [
							{
								on: "hover",
								style: {
									itemOpacity: 1,
								},
							},
						],
						itemTextColor: "#ffffff",
					},
				]}
				barAriaLabel={function (e) {
					return (
						e.id + ": " + e.formattedValue + " in country: " + e.indexValue
					);
				}}
				isInteractive={false}
				enableGridY={false}
			/>
		</StyledTurnBarChart>
	);
};

export default TurnBarChart;
