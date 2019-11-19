-- auto-generated definition
create table crawl_block
(
    id               bigint auto_increment
        primary key,
    city_code        varchar(20)  null,
    platform_id      tinyint      null,
    block_name       varchar(200) null,
    block_id         varchar(50)  null,
    local_block_name varchar(200) null,
    local_block_id   varchar(50)  null,
    create_date      datetime     null,
    update_date      datetime     null,
    constraint city_code
        unique (city_code, platform_id, block_id)
)
    engine = InnoDB;


create table crawl_block_compare
(
    id               bigint auto_increment
        primary key,
    cityCode         varchar(20)                         null,
    platformId       tinyint                             null,
    blockName        varchar(200)                        null,
    blockId          varchar(50)                         null,
    local_block_name varchar(200)                        null,
    local_block_id   varchar(50)                         null,
    create_date      timestamp default CURRENT_TIMESTAMP not null,
    constraint city_code
        unique (cityCode, platformId, blockId)
)
    engine = InnoDB;


-- auto-generated definition
create table crawl_sell
(
    id                  bigint auto_increment
        primary key,
    city_code           varchar(20)    null,
    platform_id         tinyint        null,
    house_id            varchar(50)    null,
    url                 varchar(200)   null,
    title               varchar(200)   null,
    district            varchar(50)    null,
    sub_district        varchar(50)    null,
    block_name          varchar(100)   null,
    block_id            varchar(50)    null,
    total_price         decimal(10, 2) null,
    unit_price          decimal(10, 2) null,
    room_count          tinyint        null,
    hall_count          tinyint        null,
    toilet_count        tinyint        null,
    total_floor         tinyint        null,
    floor_code          tinyint        null,
    forward             varchar(20)    null,
    decoration          varchar(20)    null,
    build_area          decimal(10, 2) null,
    build_year          smallint(6)    null,
    has_lift            tinyint        null,
    property_right_year tinyint        null,
    list_time           varchar(8)     null,
    create_date         datetime       null,
    update_date         datetime       null,
    constraint city_code
        unique (city_code, platform_id, house_id)
)
    engine = InnoDB;


-- auto-generated definition
create table crawl_sell_compare
(
    id                bigint auto_increment
        primary key,
    cityCode          varchar(20)                         null,
    platformId        tinyint                             null comment '1 贝壳 2 链家 3 安居客 4 21世纪 5 我爱我家',
    houseId           varchar(50)                         null,
    url               varchar(200)                        null,
    title             varchar(200)                        null,
    district          varchar(50)                         null,
    subDistrict       varchar(50)                         null,
    blockName         varchar(100)                        null,
    blockId           varchar(50)                         null,
    totalPrice        decimal(10, 2)                      null,
    unitPrice         decimal(10, 2)                      null,
    roomCount         tinyint                             null,
    hallCount         tinyint                             null,
    toiletCount       tinyint                             null,
    totalFloor        tinyint                             null,
    floorCode         tinyint                             null,
    forward           varchar(20)                         null,
    decoration        varchar(20)                         null,
    buildArea         decimal(10, 2)                      null,
    buildYear         smallint(6)                         null,
    hasLift           tinyint                             null,
    propertyRightYear tinyint                             null,
    listTime          varchar(8)                          null,
    official_id       varchar(10)                         null,
    percent           varchar(10)                         null,
    create_time       timestamp default CURRENT_TIMESTAMP null comment '创建时间',
    constraint city_code
        unique (cityCode, platformId, houseId)
)
    engine = InnoDB;

create table crawl_relation
(
    id               bigint auto_increment primary key,
    crawl_id         varchar(50)                         null,
    official_id       varchar(50)                             null,
    precent        varchar(50)                        null
)engine = InnoDB;




