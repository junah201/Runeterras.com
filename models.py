from sqlalchemy import Column, String, Integer, DateTime, JSON, ForeignKey, BOOLEAN, func, VARCHAR, VARCHAR, DATE
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import INTEGER
from database import Base, engine


class Player(Base):
    __tablename__ = "player"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = Column(
        INTEGER(unsigned=True),
        primary_key=True,
        unique=True,
        nullable=False,
        comment="유저 고유 번호",
    )
    puuid = Column(
        VARCHAR(150),
        unique=True,
        nullable=True,
        comment="유저 puuid 번호",
    )
    game_name = Column(
        VARCHAR(50),
        unique=False,
        nullable=False,
        comment="유저 이름",
    )
    tag_line = Column(
        VARCHAR(10),
        unique=False,
        nullable=True,
        comment="유저 태그라인",
    )
    is_master = Column(
        BOOLEAN,
        unique=False,
        nullable=False,
        default=False,
        comment="마스터 여부",
    )
    last_matched_at = Column(
        DateTime,
        unique=False,
        nullable=True,
        comment="마지막 매치 시간",
    )
    last_matched_game_id = Column(
        VARCHAR(40),
        unique=False,
        nullable=True,
        comment="마지막 매치 게임 아이디",
    )
    last_checked_at = Column(
        DateTime,
        unique=False,
        nullable=True,
        comment="마지막 체크 시간",
    )
    last_used_deck_code = Column(
        VARCHAR(100),
        unique=False,
        nullable=True,
        comment="마지막 사용한 덱 아이디",
    )
    created_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        comment="생성 시점"
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
        comment="마지막 수정 시점"
    )

    def __repr__(self):
        return f"Player(id={self.id}, game_name={self.game_name}, tag_line={self.tag_line}, is_master={self.is_master}, last_matched_at={self.last_matched_at}, last_matched_game_id={self.last_matched_game_id}, last_checked_at={self.last_checked_at}, last_used_deck_code={self.last_used_deck_code}, created_at={self.created_at}, updated_at={self.updated_at})"

    def __str__(self):
        return f"Player(id={self.id}, game_name={self.game_name}, tag_line={self.tag_line}, is_master={self.is_master}, last_matched_at={self.last_matched_at}, last_matched_game_id={self.last_matched_game_id}, last_checked_at={self.last_checked_at}, last_used_deck_code={self.last_used_deck_code}, created_at={self.created_at}, updated_at={self.updated_at})"


class DataVersion(Base):
    __tablename__ = "data_version"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    data_version = Column(
        VARCHAR(30),
        primary_key=True,
        unique=True,
        nullable=False,
        comment="데이터 버전 고유 번호",
    )
    total_match_count = Column(
        INTEGER(unsigned=True),
        unique=False,
        nullable=False,
        default=0,
        comment="전체 매치 수",
    )
    created_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        comment="생성 시점"
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
        comment="마지막 수정 시점"
    )

    def __repr__(self):
        return f"DataVersion(data_version={self.data_version}, total_match_count={self.total_match_count}, created_at={self.created_at}, updated_at={self.updated_at})"

    def __str__(self):
        return f"DataVersion(data_version={self.data_version}, total_match_count={self.total_match_count}, created_at={self.created_at}, updated_at={self.updated_at})"


class SingleMetaDeckAnalyze(Base):
    __tablename__ = "single_meta_deck_analyze"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = Column(
        INTEGER(unsigned=True),
        primary_key=True,
        unique=True,
        nullable=False,
        comment="단일 덱 분석 고유 번호",
    )
    data_version = Column(
        VARCHAR(30),
        ForeignKey("data_version.data_version"),
        nullable=False,
        comment="데이터 버전 고유 번호",
    )
    win_count = Column(
        INTEGER(unsigned=True),
        unique=False,
        nullable=False,
        default=0,
        comment="승리 수",
    )
    lose_count = Column(
        INTEGER(unsigned=True),
        unique=False,
        nullable=False,
        default=0,
        comment="패배 수",
    )

    def __repr__(self):
        return f"SingleMetaDeckAnalyze(id={self.id}, data_version={self.data_version}, win_count={self.win_count}, lose_count={self.lose_count})"

    def __str__(self):
        return f"SingleMetaDeckAnalyze(id={self.id}, data_version={self.data_version}, win_count={self.win_count}, lose_count={self.lose_count})"


class SingleMetaDeckFaction(Base):
    __tablename__ = "single_meta_deck_faction"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = Column(
        INTEGER(unsigned=True),
        primary_key=True,
        unique=True,
        nullable=False,
        comment="덱 지역 고유 번호",
    )
    name = Column(
        VARCHAR(100),
        nullable=False,
        comment="덱 지역 이름",
    )
    single_meta_deck_analyze_id = Column(
        INTEGER(unsigned=True),
        ForeignKey("single_meta_deck_analyze.id"),
        nullable=False,
        comment="단일 덱 분석 고유 번호",
    )

    def __repr__(self):
        return f"SingleMetaDeckFaction(id={self.id}, name={self.name}, single_meta_deck_analyze_id={self.single_meta_deck_analyze_id})"

    def __str__(self):
        return f"SingleMetaDeckFaction(id={self.id}, name={self.name}, single_meta_deck_analyze_id={self.single_meta_deck_analyze_id})"


class SingleMetaDeckChampion(Base):
    __tablename__ = "single_meta_deck_champion"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = Column(
        INTEGER(unsigned=True),
        primary_key=True,
        unique=True,
        nullable=False,
        comment="챔피언 고유 번호",
    )
    name = Column(
        VARCHAR(100),
        nullable=False,
        comment="챔피언 이름",
    )
    single_meta_deck_analyze_id = Column(
        INTEGER(unsigned=True),
        ForeignKey("single_meta_deck_analyze.id"),
        nullable=False,
        comment="단일 덱 분석 고유 번호",
    )

    def __repr__(self):
        return f"SingleMetaDeckChampion(id={self.id}, name={self.name}, single_meta_deck_analyze_id={self.single_meta_deck_analyze_id})"

    def __str__(self):
        return f"SingleMetaDeckChampion(id={self.id}, name={self.name}, single_meta_deck_analyze_id={self.single_meta_deck_analyze_id})"


class SingleMetaDeckCodeAnalyze(Base):
    __tablename__ = "single_meta_deck_code_analyze"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = Column(
        INTEGER(unsigned=True),
        primary_key=True,
        unique=True,
        nullable=False,
        comment="단일 덱 코드 분석 고유 번호",
    )
    data_version = Column(
        VARCHAR(30),
        ForeignKey("data_version.data_version"),
        nullable=False,
        comment="데이터 버전 고유 번호",
    )
    deck_code = Column(
        VARCHAR(100),
        nullable=False,
        comment="덱 코드",
    )
    win_count = Column(
        INTEGER(unsigned=True),
        unique=False,
        nullable=False,
        default=0,
        comment="승리 수",
    )
    lose_count = Column(
        INTEGER(unsigned=True),
        unique=False,
        nullable=False,
        default=0,
        comment="패배 수",
    )

    def __repr__(self):
        return f"SingleMetaDeckCodeAnalyze(id={self.id}, data_version={self.data_version}, deck_code={self.deck_code}, win_count={self.win_count}, lose_count={self.lose_count})"

    def __str__(self):
        return f"SingleMetaDeckCodeAnalyze(id={self.id}, data_version={self.data_version}, deck_code={self.deck_code}, win_count={self.win_count}, lose_count={self.lose_count})"


class DoubleMetaDeckCodeAnalyze(Base):
    __tablename__ = "double_meta_deck_code_analyze"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = Column(
        INTEGER(unsigned=True),
        primary_key=True,
        unique=True,
        nullable=False,
        comment="다중 덱 코드 분석 고유 번호",
    )
    data_version = Column(
        VARCHAR(30),
        ForeignKey("data_version.data_version"),
        nullable=False,
        comment="데이터 버전 고유 번호",
    )
    my_deck_id = Column(
        INTEGER(unsigned=True),
        ForeignKey("single_meta_deck_code_analyze.id"),
        nullable=False,
        comment="단일 덱 분석 고유 번호",
    )
    opponent_deck_id = Column(
        INTEGER(unsigned=True),
        ForeignKey("single_meta_deck_code_analyze.id"),
        nullable=False,
        comment="상대 방 단일 덱 분석 고유 번호",
    )
    win_count = Column(
        INTEGER(unsigned=True),
        unique=False,
        nullable=False,
        default=0,
        comment="승리 수",
    )
    lose_count = Column(
        INTEGER(unsigned=True),
        unique=False,
        nullable=False,
        default=0,
        comment="패배 수",
    )

    def __repr__(self):
        return f"DoubleMetaDeckCodeAnalyze(id={self.id}, data_version={self.data_version}, my_deck_id={self.my_deck_id}, opponent_deck_id={self.opponent_deck_id}, win_count={self.win_count}, lose_count={self.lose_count})"

    def __str__(self):
        return f"DoubleMetaDeckCodeAnalyze(id={self.id}, data_version={self.data_version}, my_deck_id={self.my_deck_id}, opponent_deck_id={self.opponent_deck_id}, win_count={self.win_count}, lose_count={self.lose_count})"


Base.metadata.create_all(bind=engine)
