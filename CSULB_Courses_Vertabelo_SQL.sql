-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2024-12-09 17:58:41.907

-- tables
-- Table: choices
CREATE TABLE choices (
    name varchar(30)  NOT NULL,
    CONSTRAINT choices_pk PRIMARY KEY (name)
);

-- Table: course_requirements
CREATE TABLE course_requirements (
    requirement_name varchar(30)  NOT NULL,
    course_name varchar(30)  NOT NULL,
    CONSTRAINT course_requirements_pk PRIMARY KEY (requirement_name,course_name)
);

-- Table: courses
CREATE TABLE courses (
    name varchar(30)  NOT NULL,
    departments_abbr varchar(50)  NOT NULL,
    number int  NOT NULL,
    description varchar(100)  NOT NULL,
    units int  NOT NULL,
    CONSTRAINT courses_uk_01 UNIQUE (departments_abbr, number) NOT DEFERRABLE  INITIALLY IMMEDIATE,
    CONSTRAINT courses_pk PRIMARY KEY (name)
);

-- Table: departments
CREATE TABLE departments (
    name varchar(50)  NOT NULL,
    abbreviation varchar(4)  NOT NULL,
    CONSTRAINT departments_uk_01 UNIQUE (abbreviation) NOT DEFERRABLE  INITIALLY IMMEDIATE,
    CONSTRAINT departments_pk PRIMARY KEY (name)
);

-- Table: majors
CREATE TABLE majors (
    name varchar(30)  NOT NULL,
    departments_name varchar(50)  NOT NULL,
    description varchar(100)  NOT NULL,
    CONSTRAINT majors_pk PRIMARY KEY (name)
);

-- Table: mandatories
CREATE TABLE mandatories (
    name varchar(30)  NOT NULL,
    CONSTRAINT mandatories_pk PRIMARY KEY (name)
);

-- Table: requirements
CREATE TABLE requirements (
    name varchar(30)  NOT NULL,
    majors_name varchar(30)  NOT NULL,
    description varchar(100)  NOT NULL,
    credits int  NOT NULL,
    CONSTRAINT requirements_pk PRIMARY KEY (name)
);

-- Table: totals
CREATE TABLE totals (
    name varchar(30)  NOT NULL,
    CONSTRAINT totals_pk PRIMARY KEY (name)
);

-- foreign keys
-- Reference: choices_requirements (table: choices)
ALTER TABLE choices ADD CONSTRAINT choices_requirements
    FOREIGN KEY (name)
    REFERENCES requirements (name)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: course_requirements_courses (table: course_requirements)
ALTER TABLE course_requirements ADD CONSTRAINT course_requirements_courses
    FOREIGN KEY (course_name)
    REFERENCES courses (name)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: course_requirements_requirements (table: course_requirements)
ALTER TABLE course_requirements ADD CONSTRAINT course_requirements_requirements
    FOREIGN KEY (requirement_name)
    REFERENCES requirements (name)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: courses_departments (table: courses)
ALTER TABLE courses ADD CONSTRAINT courses_departments
    FOREIGN KEY (departments_abbr)
    REFERENCES departments (abbreviation)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: majors_departments (table: majors)
ALTER TABLE majors ADD CONSTRAINT majors_departments
    FOREIGN KEY (departments_name)
    REFERENCES departments (name)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: mandatories_requirements (table: mandatories)
ALTER TABLE mandatories ADD CONSTRAINT mandatories_requirements
    FOREIGN KEY (name)
    REFERENCES requirements (name)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: requirements_majors (table: requirements)
ALTER TABLE requirements ADD CONSTRAINT requirements_majors
    FOREIGN KEY (majors_name)
    REFERENCES majors (name)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: totals_requirements (table: totals)
ALTER TABLE totals ADD CONSTRAINT totals_requirements
    FOREIGN KEY (name)
    REFERENCES requirements (name)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

