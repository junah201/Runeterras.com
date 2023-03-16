import { Link } from "react-router-dom";
import styled from "styled-components";

const StyledFooter = styled.footer`
	display: flex;
	align-items: center;
	justify-content: center;
	height: 400px;
	background-color: #262161;
	border-top: 1px solid #534ac1;
	padding: 75px 0;
`;

const StyledFooterItemContainer = styled.div`
	display: flex;
	flex-direction: row;
	justify-content: center;
`;

const StyledFooterItem = styled.div`
	display: flex;
	flex-direction: column;
	min-width: 150px;

	& span {
		color: #ffffff;
		font-size: 16px;
		font-weight: bold;

		margin-bottom: 20px;
	}

	& a {
		color: #ffffff;
		font-size: 12px;
		font-weight: regular;
		text-decoration: none;

		& img {
			color: #ffffff;
		}
	}

	& p {
		color: #ffffff;
		font-size: 12px;
		font-weight: regular;
		text-decoration: none;

		& img {
			color: #ffffff;
		}
	}

	& a:hover {
		text-decoration: underline;
	}
`;

const StyledFooterDivider = styled.div`
	width: 1px;
	height: 250px;
	background-color: #534ac1;
	margin: 0 150px;
`;

const Footer: React.FC = () => {
	return (
		<StyledFooter>
			<StyledFooterItemContainer>
				<StyledFooterItem>
					<span>정보</span>
					<a href="https://github.com/junah201/Runeterras.com">
						Github <img src="link.svg" alt="" />
					</a>
					<a href="https://github.com/junah201/Runeterras.com">
						업데이트 <img src="link.svg" alt="" />
					</a>
					<a href="https://github.com/junah201/Runeterras.com">
						이슈 트래커 <img src="link.svg" alt="" />
					</a>
				</StyledFooterItem>
				<StyledFooterItem>
					<span>커뮤니티</span>
					<a href="https://discord.gg/g47sMgKTWA">
						Discord 서버 <img src="link.svg" alt="" />
					</a>
				</StyledFooterItem>
				<StyledFooterItem>
					<span>도움말</span>
					<Link to="/help/rules">규칙</Link>
					<Link to="/help/tos">이용약관</Link>
					<Link to="/help/privacy">개인정보 처리방침</Link>
				</StyledFooterItem>
			</StyledFooterItemContainer>
			<StyledFooterDivider />
			<StyledFooterItemContainer>
				<StyledFooterItem>
					<span>Runeterras.com</span>
					<p>© 2023 - 2023.</p>
					<p>
						`Runeterras.com`은{" "}
						<a href="https://github.com/junah201">
							Junah201 <img src="link.svg" alt="" />
						</a>
						가 독립적으로 운영하고 있습니다.
					</p>
					<p>
						`Runeterra``, `Legends of Runeterra` 는 라이엇게임즈의 상표입니다.
					</p>
				</StyledFooterItem>
			</StyledFooterItemContainer>
		</StyledFooter>
	);
};

export default Footer;
