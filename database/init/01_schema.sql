
create table simple_blog
(
    id            serial
        constraint blog_pk
            primary key,
    title         varchar(48)                    not null,
    post          text,
    creation_date date default current_timestamp not null
);
