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
