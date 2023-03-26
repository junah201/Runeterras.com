import { Link, NavLink } from "react-router-dom";
import styled from "styled-components";

const StyledHeader = styled.header`
	display: flex;
	align-items: center;
	height: 100px;
	background-color: #262161;
	border-bottom: 1px solid #534ac1;
	padding: 0 100px;

	& nav {
		display: flex;
		align-items: center;
		justify-content: center;
		justify-items: center;
		margin: 0 100px;

		& a {
			color: #ffffff;
			text-decoration: none;
			font-size: 1.5rem;
			font-weight: bold;
		}

		& a + a {
			margin-left: 30px;
		}
	}

	& div {
		margin-left: auto;

		& a {
			color: #ffffff;
			text-decoration: none;
			font-size: 20px;
			font-weight: bold;
		}
	}
`;

const Header: React.FC = () => {
	return (
		<StyledHeader>
			<Link to="/">
				<img src="/logo.svg" alt="Logo" />
			</Link>
			<nav>
				<NavLink to="/deck/meta">메타 덱</NavLink>
				<NavLink to="/deck/compare">덱 비교</NavLink>
			</nav>
			<div>
				<NavLink to="/login">로그인</NavLink>
			</div>
		</StyledHeader>
	);
};

export default Header;
