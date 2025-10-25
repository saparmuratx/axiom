CREATE TABLE "users"(
    "id" UUID NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMP(0) WITH
        TIME zone NOT NULL,
        "updated_at" TIMESTAMP(0)
    WITH
        TIME zone NOT NULL,
        "password" VARCHAR(255) NOT NULL,
        "is_active" BOOLEAN NOT NULL,
        "role_id" UUID NOT NULL
);
CREATE INDEX "users_email_index" ON
    "users"("email");
ALTER TABLE
    "users" ADD PRIMARY KEY("id");
ALTER TABLE
    "users" ADD CONSTRAINT "users_email_unique" UNIQUE("email");
CREATE TABLE "profiles"(
    "id" UUID NOT NULL,
    "account_id" UUID NOT NULL,
    "first_name" VARCHAR(255) NOT NULL,
    "last_name" VARCHAR(255) NOT NULL,
    "phone_number" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMP(0) WITH
        TIME zone NOT NULL,
        "updated_at" TIMESTAMP(0)
    WITH
        TIME zone NOT NULL
);
ALTER TABLE
    "profiles" ADD PRIMARY KEY("id");
ALTER TABLE
    "profiles" ADD CONSTRAINT "profiles_account_id_unique" UNIQUE("account_id");
CREATE TABLE "roles"(
    "id" UUID NOT NULL,
    "title" VARCHAR(255) NOT NULL,
    "description" VARCHAR(255) NOT NULL,
    "permissions" jsonb NOT NULL,
    "created_at" TIMESTAMP(0) WITH
        TIME zone NOT NULL,
        "updated_at" TIMESTAMP(0)
    WITH
        TIME zone NOT NULL
);
ALTER TABLE
    "roles" ADD PRIMARY KEY("id");
COMMENT
ON COLUMN
    "roles"."permissions" IS '{"auth:accounts": {"read": true, "create": true, "update": true, "delete": true}, "library:books": {"read": true, "create": true}}';
CREATE TABLE "book"(
    "id" UUID NOT NULL,
    "title" VARCHAR(255) NOT NULL,
    "published_at" TIMESTAMP(0) WITH
        TIME zone NOT NULL,
        "created_at" TIMESTAMP(0)
    WITH
        TIME zone NOT NULL,
        "updated_at" TIMESTAMP(0)
    WITH
        TIME zone NOT NULL,
        "edition" VARCHAR(255) NOT NULL,
        "author_id" UUID NOT NULL
);
ALTER TABLE
    "book" ADD PRIMARY KEY("id");
ALTER TABLE
    "book" ADD CONSTRAINT "book_title_unique" UNIQUE("title");
CREATE TABLE "author"(
    "id" UUID NOT NULL,
    "first_name" VARCHAR(255) NOT NULL,
    "last_name" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMP(0) WITH
        TIME zone NOT NULL,
        "updated_at" TIMESTAMP(0)
    WITH
        TIME zone NOT NULL
);
ALTER TABLE
    "author" ADD PRIMARY KEY("id");
CREATE TABLE "collectionbook"(
    "id" UUID NOT NULL,
    "book_id" UUID NOT NULL,
    "collection_id" UUID NOT NULL,
    "created_at" TIMESTAMP(0) WITH
        TIME zone NOT NULL,
        "updated_at" TIMESTAMP(0)
    WITH
        TIME zone NOT NULL
);
ALTER TABLE
    "collectionbook" ADD PRIMARY KEY("id");
CREATE TABLE "collection"(
    "id" UUID NOT NULL,
    "title" VARCHAR(255) NOT NULL,
    "description" VARCHAR(255) NOT NULL,
    "user_id" UUID NOT NULL,
    "is_public" BOOLEAN NOT NULL,
    "created_at" TIMESTAMP(0) WITH
        TIME zone NOT NULL,
        "updated_at" TIMESTAMP(0)
    WITH
        TIME zone NOT NULL
);
ALTER TABLE
    "collection" ADD PRIMARY KEY("id");
CREATE TABLE "favorites"(
    "id" UUID NOT NULL,
    "book_id" UUID NOT NULL,
    "user_id" UUID NOT NULL,
    "created_at" TIMESTAMP(0) WITH
        TIME zone NOT NULL,
        "updated_at" TIMESTAMP(0)
    WITH
        TIME zone NOT NULL
);
ALTER TABLE
    "favorites" ADD PRIMARY KEY("id");
CREATE TABLE "bookgenre"(
    "id" UUID NOT NULL,
    "book_id" UUID NOT NULL,
    "genre_id" UUID NOT NULL,
    "created_at" TIMESTAMP(0) WITH
        TIME zone NOT NULL,
        "updated_at" TIMESTAMP(0)
    WITH
        TIME zone NOT NULL
);
ALTER TABLE
    "bookgenre" ADD PRIMARY KEY("id");
CREATE TABLE "genre"(
    "id" UUID NOT NULL,
    "title" VARCHAR(255) NOT NULL,
    "description" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMP(0) WITH
        TIME zone NOT NULL,
        "updated_at" TIMESTAMP(0)
    WITH
        TIME zone NOT NULL
);
ALTER TABLE
    "genre" ADD PRIMARY KEY("id");
CREATE TABLE "readingprogress"(
    "id" UUID NOT NULL,
    "user_id" UUID NOT NULL,
    "book_id" VARCHAR(255) NOT NULL,
    "chapter_id" UUID NOT NULL,
    "chunk_id" UUID NOT NULL,
    "offset" INTEGER NOT NULL,
    "created_at" TIMESTAMP(0) WITH
        TIME zone NOT NULL,
        "updated_at" TIMESTAMP(0)
    WITH
        TIME zone NOT NULL
);
ALTER TABLE
    "readingprogress" ADD PRIMARY KEY("id");

CREATE TABLE "highlight"(
    "id" UUID NOT NULL,
    "book_id" UUID NOT NULL,
    "chapter_id" UUID NOT NULL,
    "chunk_id" UUID NOT NULL,
    "offset_start" INTEGER NOT NULL,
    "offset_end" INTEGER NOT NULL,
    "created_at" TIMESTAMP(0) WITH
        TIME zone NOT NULL,
        "updated_at" TIMESTAMP(0)
    WITH
        TIME zone NOT NULL
);
ALTER TABLE
    "highlight" ADD PRIMARY KEY("id");

CREATE TABLE "note"(
    "id" UUID NOT NULL,
    "book_id" UUID NOT NULL,
    "chapter_id" UUID NOT NULL,
    "chunk_id" UUID NOT NULL,
    "offset_start" INTEGER NOT NULL,
    "offset_end" INTEGER NOT NULL,
    "created_at" TIMESTAMP(0) WITH
        TIME zone NOT NULL,
        "updated_at" TIMESTAMP(0)
    WITH
        TIME zone NOT NULL,
        "note_text" VARCHAR(255) NOT NULL
);

ALTER TABLE
    "note" ADD PRIMARY KEY("id");


CREATE TABLE "chapter"(
    "id" UUID NOT NULL,
    "book_id" UUID NOT NULL,
    "title" VARCHAR(255) NOT NULL,
    "number" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMP(0) WITH
        TIME zone NOT NULL,
        "updated_at" TIMESTAMP(0)
    WITH
        TIME zone NOT NULL,
        "prev_chapter" UUID NOT NULL,
        "next_chapter" UUID NOT NULL
);
ALTER TABLE
    "chapter" ADD PRIMARY KEY("id");

CREATE TABLE "chunk"(
    "id" UUID NOT NULL,
    "chapter_id" UUID NOT NULL,
    "size" INTEGER NOT NULL,
    "created_at" TIMESTAMP(0) WITH
        TIME zone NOT NULL,
        "updated_at" TIMESTAMP(0)
    WITH
        TIME zone NOT NULL,
        "prev_chunk" UUID NOT NULL,
        "next_chunk" UUID NOT NULL
);

ALTER TABLE
    "chunk" ADD PRIMARY KEY("id");

ALTER TABLE
    "chunk" ADD CONSTRAINT "chunk_chapter_id_foreign" FOREIGN KEY("chapter_id") REFERENCES "chapter"("id");
    

ALTER TABLE
    "book" ADD CONSTRAINT "book_author_id_foreign" FOREIGN KEY("author_id") REFERENCES "author"("id");
ALTER TABLE
    "favorites" ADD CONSTRAINT "favorites_book_id_foreign" FOREIGN KEY("book_id") REFERENCES "book"("id");
ALTER TABLE
    "bookgenre" ADD CONSTRAINT "bookgenre_genre_id_foreign" FOREIGN KEY("genre_id") REFERENCES "genre"("id");
ALTER TABLE
    "note" ADD CONSTRAINT "note_book_id_foreign" FOREIGN KEY("book_id") REFERENCES "book"("id");
ALTER TABLE
    "collectionbook" ADD CONSTRAINT "collectionbook_collection_id_foreign" FOREIGN KEY("collection_id") REFERENCES "collection"("id");
ALTER TABLE
    "readingprogress" ADD CONSTRAINT "readingprogress_book_id_foreign" FOREIGN KEY("book_id") REFERENCES "book"("id");
ALTER TABLE
    "highlight" ADD CONSTRAINT "highlight_book_id_foreign" FOREIGN KEY("book_id") REFERENCES "book"("id");

ALTER TABLE
    "users" ADD CONSTRAINT "users_role_id_foreign" FOREIGN KEY("role_id") REFERENCES "roles"("id");
ALTER TABLE
    "bookgenre" ADD CONSTRAINT "bookgenre_book_id_foreign" FOREIGN KEY("book_id") REFERENCES "book"("id");
ALTER TABLE
    "profiles" ADD CONSTRAINT "profiles_account_id_foreign" FOREIGN KEY("account_id") REFERENCES "users"("id");
ALTER TABLE
    "collectionbook" ADD CONSTRAINT "collectionbook_book_id_foreign" FOREIGN KEY("book_id") REFERENCES "book"("id");