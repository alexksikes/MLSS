create table applicants (
    id                      int(11) not null auto_increment primary key,
    first_name              varchar(100),
    last_name               varchar(100),
    email                   varchar(100) not null unique,
    website                 varchar(250),
    affiliation             varchar(100),
    affiliated              boolean default false,
    department              varchar(100),
    interests               text,
    degree                  varchar(50),
    occupation              varchar(50),
    resume_fn               varchar(100),

    gender                  enum('male', 'female'),
    nationality             varchar(100),
    country                 varchar(100),
    pascal_member           boolean default false,
    poster_title            varchar(250),
    abstract                text,
    cover_letter            text,
    
    travel_support          boolean default false,
    travel_support_budget   int(5) default 0,
    grant_amount        	int(11) default 0,
    granted_by_user_id    	int(11),            
    
    secret_md5              varchar(35),
    referee_name            varchar(100),
    referee_email           varchar(100),
    referee_affiliation     varchar(100),
    
    reference_fn            varchar(100),
    reference               text,
    referee_rating          tinyint(4),
    
    status                  enum('admitted', 'rejected'),
    decided_by_user_id      int(11),

    calculated_vote         float,
    calculated_vote_counts  int(11),
    
    creation_ts             timestamp default current_timestamp, 
    update_ts               timestamp,
    index(secret_md5)
) engine=InnoDB charset utf8;

create table users (
    id                      int(11) not null auto_increment primary key,
    email                   varchar(100) not null unique,
    password                varchar(35) not null,
    nickname                varchar(35) not null
) engine=InnoDB charset utf8;

create table votes (
    user_id                 int(11) not null,
    applicant_id            int(11) not null,
    score                   tinyint(4),
    creation_ts             timestamp default current_timestamp,
    primary key             (user_id, applicant_id)
) engine=InnoDB charset utf8;

create table comments (
    id                      int(11) not null auto_increment primary key,
    user_id                 int(11) not null,
    applicant_id            int(11) not null,
    comment                 text,
    creation_ts             timestamp default current_timestamp 
) engine=InnoDB charset utf8;

create table sessions (
    session_id              char(128) unique not null,
    atime                   timestamp not null default current_timestamp,
    data                    text
) engine=InnoDB charset utf8;

alter table applicants add index(decided_by_user_id);
alter table comments add index(user_id);
alter table comments add index(applicant_id);
alter table votes add index(user_id);
alter table votes add index(applicant_id);
