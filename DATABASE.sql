
CREATE TABLE public.sightings (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    date DATE NOT NULL,
    "time" TIME NOT NULL,
    room TEXT NOT NULL
);


