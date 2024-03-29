from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, BOOLEAN, func, VARCHAR, VARCHAR, DATETIME
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import INTEGER, JSON
from sqlalchemy.ext.mutable import MutableDict
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
        VARCHAR(1023),
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


class GameVersion(Base):
    __tablename__ = "game_version"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    game_version = Column(
        VARCHAR(30),
        primary_key=True,
        unique=True,
        nullable=False,
        comment="게임 버전 고유 번호",
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
        return f"GameVersion(game_version={self.game_version}, total_match_count={self.total_match_count}, created_at={self.created_at}, updated_at={self.updated_at})"

    def __str__(self):
        return f"GameVersion(game_version={self.game_version}, total_match_count={self.total_match_count}, created_at={self.created_at}, updated_at={self.updated_at})"


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
    game_version = Column(
        VARCHAR(30),
        ForeignKey("game_version.game_version"),
        nullable=False,
        comment="데이터 버전 고유 번호",
    )
    deck_code = Column(
        VARCHAR(1023),
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
    first_start_win_count = Column(
        INTEGER(unsigned=True),
        unique=False,
        nullable=False,
        default=0,
        comment="선공 승리 수",
    )
    first_start_lose_count = Column(
        INTEGER(unsigned=True),
        unique=False,
        nullable=False,
        default=0,
        comment="선공 패배 수",
    )
    turns = Column(
        MutableDict.as_mutable(JSON),
        unique=False,
        nullable=True,
        default=dict(),
        comment="턴별 분석",
    )

    def __repr__(self):
        return f"SingleMetaDeckAnalyze(id={self.id}, game_version={self.game_version}, win_count={self.win_count}, lose_count={self.lose_count} first_start_win_count={self.first_start_win_count}, first_start_lose_count={self.first_start_lose_count})"

    def __str__(self):
        return f"SingleMetaDeckAnalyze(id={self.id}, game_version={self.game_version}, win_count={self.win_count}, lose_count={self.lose_count} first_start_win_count={self.first_start_win_count}, first_start_lose_count={self.first_start_lose_count})"


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
    single_meta_deck_analyze_id = Column(
        INTEGER(unsigned=True),
        ForeignKey("single_meta_deck_analyze.id"),
        nullable=False,
        comment="단일 덱 분석 고유 번호",
    )
    deck_code = Column(
        VARCHAR(1023),
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
        return f"SingleMetaDeckCodeAnalyze(id={self.id}, single_meta_deck_analyze_id={self.single_meta_deck_analyze_id}, deck_code={self.deck_code}, win_count={self.win_count}, lose_count={self.lose_count})"

    def __str__(self):
        return f"SingleMetaDeckCodeAnalyze(id={self.id}, single_meta_deck_analyze_id={self.single_meta_deck_analyze_id}, deck_code={self.deck_code}, win_count={self.win_count}, lose_count={self.lose_count})"


class DoubleMetaDeckAnalyze(Base):
    __tablename__ = "double_meta_deck_analyze"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = Column(
        INTEGER(unsigned=True),
        primary_key=True,
        unique=True,
        nullable=False,
        comment="다중 덱 코드 분석 고유 번호",
    )
    my_deck_id = Column(
        INTEGER(unsigned=True),
        ForeignKey("single_meta_deck_analyze.id"),
        nullable=False,
        comment="단일 덱 분석 고유 번호",
    )
    opponent_deck_id = Column(
        INTEGER(unsigned=True),
        ForeignKey("single_meta_deck_analyze.id"),
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
    first_start_win_count = Column(
        INTEGER(unsigned=True),
        unique=False,
        nullable=False,
        default=0,
        comment="선공 승리 수",
    )
    first_start_lose_count = Column(
        INTEGER(unsigned=True),
        unique=False,
        nullable=False,
        default=0,
        comment="선공 패배 수",
    )
    turns = Column(
        MutableDict.as_mutable(JSON),
        unique=False,
        nullable=True,
        default=dict(),
        comment="턴별 분석",
    )

    my_deck = relationship("SingleMetaDeckAnalyze", foreign_keys=[
                           my_deck_id], lazy="joined")
    opponent_deck = relationship("SingleMetaDeckAnalyze", foreign_keys=[
                                 opponent_deck_id], lazy="joined")

    def __repr__(self):
        return f"DoubleMetaDeckAnalyze(id={self.id}, my_deck_id={self.my_deck_id}, opponent_deck_id={self.opponent_deck_id}, win_count={self.win_count}, lose_count={self.lose_count}) first_start_win={self.first_start_win_count} first_start_lose={self.first_start_lose_count})"

    def __str__(self):
        return f"DoubleMetaDeckAnalyze(id={self.id}, my_deck_id={self.my_deck_id}, opponent_deck_id={self.opponent_deck_id}, win_count={self.win_count}, lose_count={self.lose_count}) first_start_win={self.first_start_win_count} first_start_lose={self.first_start_lose_count})"


class Card(Base):
    __tablename__ = "card"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = Column(
        VARCHAR(20),
        primary_key=True,
        unique=True,
        nullable=False,
        index=True,
        comment="카드 고유 번호",
    )
    name = Column(
        VARCHAR(100),
        nullable=False,
        comment="카드 이름 (영문)",
    )
    region = Column(
        VARCHAR(30),
        nullable=False,
        comment="카드 지역",
    )
    type = Column(
        VARCHAR(20),
        nullable=False,
        comment="카드 타입",
    )
    set = Column(
        VARCHAR(20),
        nullable=False,
        comment="카드 세트",
    )
    is_champion = Column(
        BOOLEAN,
        nullable=False,
        default=False,
        comment="챔피언 여부",
    )

    def __repr__(self):
        return f"Card(id={self.id}, name={self.name}, region={self.region}, type={self.type}, set={self.set})"

    def __str__(self):
        return f"Card(id={self.id}, name={self.name}, region={self.region}, type={self.type}, set={self.set})"


Base.metadata.create_all(bind=engine)
