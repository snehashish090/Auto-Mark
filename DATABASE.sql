-- SEQUENCES
CREATE SEQUENCE public.admin_auth_id_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE public.face_profiles_id_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE public.sightings_id_seq START WITH 1 INCREMENT BY 1;

-- TABLE: admin_auth
CREATE TABLE public.admin_auth (
    id integer NOT NULL DEFAULT nextval('public.admin_auth_id_seq'),
    user_id text NOT NULL,
    password text NOT NULL,
    auth_level integer NOT NULL,
    PRIMARY KEY (id)
);

-- TABLE: face_profiles
CREATE TABLE public.face_profiles (
    id integer NOT NULL DEFAULT nextval('public.face_profiles_id_seq'),
    name text NOT NULL,
    encoding double precision[] NOT NULL,
    PRIMARY KEY (id)
);

-- TABLE: sightings
CREATE TABLE public.sightings (
    id integer NOT NULL DEFAULT nextval('public.sightings_id_seq'),
    name text NOT NULL,
    date date NOT NULL,
    "time" time without time zone NOT NULL,
    room text NOT NULL,
    PRIMARY KEY (id)
);
