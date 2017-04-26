CREATE TABLE IF NOT EXISTS notes(
    note_id integer primary key autoincrement,
    username text not null,
    title text not null,
    content text not null,
    color text not null,
    status integer not null
);
