drop table if exists entries;
create table entry (
  id integer primary key autoincrement,
  title text not null,
  description text not null
);