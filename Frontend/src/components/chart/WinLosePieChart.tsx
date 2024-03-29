import React from "react";
import { ResponsivePie } from "@nivo/pie";
import styled from "styled-components";

const StyledWinLosePieChart = styled.div`
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
`;

const WinLosePieChart: React.FC<{
	title: string;
	data: object[];
	total: number;
}> = (props) => {
	return (
		<StyledWinLosePieChart>
			<span>{props.title}</span>
			<ResponsivePie
				data={props.data}
				theme={{
					labels: {
						text: {
							fill: "#ffffff",
						},
					},
				}}
				margin={{ top: 20, right: 80, bottom: 80, left: 80 }}
				innerRadius={0.4}
				padAngle={0.7}
				cornerRadius={3}
				activeOuterRadiusOffset={8}
				borderWidth={1}
				borderColor={{
					from: "color",
					modifiers: [["darker", 0.2]],
				}}
				tooltip={() => null}
				arcLabel={(d) => {
					const percent = ((d.value / props.total) * 100).toFixed(1);
					return `${d.value} (${percent}%)`;
				}}
				arcLinkLabelsSkipAngle={10}
				arcLinkLabelsTextColor="#ffffff"
				arcLinkLabelsThickness={3}
				arcLinkLabelsColor={{ from: "color" }}
			/>
		</StyledWinLosePieChart>
	);
};

export default WinLosePieChart;
