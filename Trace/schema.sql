CREATE TABLE IF NOT EXISTS decisions (
    id             TEXT PRIMARY KEY,
    statement      TEXT NOT NULL,
    discipline     TEXT,
    riba_stage     INTEGER,
    author         TEXT,                 -- JSON array of strings
    rationale      TEXT,
    assumptions    TEXT,                 -- JSON array of strings
    brief_ref      TEXT,
    importance     INTEGER,
    valid_from     TEXT,                 -- when true in the world
    valid_to       TEXT,                 -- NULL = currently valid
    recorded_at    TEXT,                 -- when the system learned it
    superseded_at  TEXT,
    superseded_by  TEXT REFERENCES decisions(id),
    status         TEXT NOT NULL DEFAULT 'valid'
                       CHECK (status IN ('valid','superseded','proposed')),
    source_episode TEXT
);

-- The decision court's record: every verdict is persisted, so the "defensible
-- record" the court produces actually exists on the trail (never deleted).
CREATE TABLE IF NOT EXISTS court_records (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    proposal_id      TEXT REFERENCES decisions(id),
    breaks_id        TEXT REFERENCES decisions(id),
    verdict          TEXT NOT NULL CHECK (verdict IN ('REJECT','ALLOW')),
    citation         TEXT,
    for_argument     TEXT,
    against_argument TEXT,
    rationale        TEXT,
    created_at       TEXT NOT NULL
);
