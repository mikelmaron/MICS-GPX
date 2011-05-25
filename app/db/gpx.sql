/* 

Create Postgis template with the following

$ POSTGIS_SQL_PATH=`pg_config --sharedir`/contrib/postgis-1.5
$ createdb -E UTF8 -T template0 template_postgis
$ createlang plpgsql template_postgis
$ psql -d template_postgis -f $POSTGIS_SQL_PATH/postgis.sql
$ psql -d template_postgis -f $POSTGIS_SQL_PATH/spatial_ref_sys.sql 

$ psql -d template_postgis
# grant select, update, insert, delete on table geometry_columns to postgres;
#grant select on table spatial_ref_sys to postgres;

Create user, and database
$ createuser gpx -P
$ createdb -T template_postgis -E UTF8 -O gpx gpx 

*/

DROP TABLE IF EXISTS gps_points;
CREATE TABLE gps_points (
    altitude double precision,
    trackid integer NOT NULL,
    gpx_id bigint NOT NULL,
    "timestamp" timestamp NOT NULL
);
SELECT AddGeometryColumn( 'gps_points', 'geom', 900913, 'POINT', 2 );

DROP TABLE IF EXISTS gpx_files;
CREATE TABLE gpx_files (
    id bigint NOT NULL,
    filename character varying(255) DEFAULT ''::character varying NOT NULL,
    size bigint,
    gps_name character varying(255) NOT NULL,
    "timestamp" timestamp NOT NULL
);
SELECT AddGeometryColumn( 'gpx_files', 'geom', 900913, 'POINT', 2 );

CREATE SEQUENCE gpx_files_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;

ALTER SEQUENCE gpx_files_id_seq OWNED BY gpx_files.id;
ALTER TABLE gpx_files ALTER ID SET DEFAULT NEXTVAL('gpx_files_id_seq');

CREATE INDEX gps_points_geom_idx ON gps_points USING GIST ( geom );
