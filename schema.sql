CREATE TABLE IF NOT EXISTS career (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(150) NOT NULL,

  CONSTRAINT career_pk PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS schedule (
  id INT NOT NULL AUTO_INCREMENT,
  start_time TIME NOT NULL,
  end_time TIME NOT NULL,
  day ENUM('Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo') NOT NULL,

  CONSTRAINT career_pk PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS student (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(75) NOT NULL,
  identification_number VARCHAR(75) NOT NULL,

  CONSTRAINT career_pk PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS teacher (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(75) NOT NULL,
  identification_number VARCHAR(75) NOT NULL,

  CONSTRAINT career_pk PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS subject (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(150) NOT NULL,
  course INT NOT NULL,
  career_id INT NOT NULL,

  CONSTRAINT career_pk PRIMARY KEY (id),

  CONSTRAINT subject_career_id_fk FOREIGN KEY (career_id)
    REFERENCES career (id)
);

CREATE TABLE IF NOT EXISTS subject_schedule (
  id INT NOT NULL AUTO_INCREMENT,
  section VARCHAR(10) NOT NULL,
  subject_id INT NOT NULL,
  schedule_id INT NOT NULL,
  teacher_id INT NOT NULL,

  CONSTRAINT career_pk PRIMARY KEY (id),

  CONSTRAINT subject_schedule_schedule_id_fk FOREIGN KEY (schedule_id)
    REFERENCES schedule (id),
  
  CONSTRAINT subject_schedule_subject_id_fk FOREIGN KEY (subject_id)
    REFERENCES subject (id),
  
  CONSTRAINT subject_schedule_teacher_id_fk FOREIGN KEY (teacher_id)
    REFERENCES teacher (id)
);

CREATE TABLE IF NOT EXISTS student_subject (
  id INT NOT NULL AUTO_INCREMENT,
  student_id INT NOT NULL,
  subject_schedule_id INT NOT NULL,

  CONSTRAINT career_pk PRIMARY KEY (id),

  CONSTRAINT student_subject_student_id_fk FOREIGN KEY (student_id)
    REFERENCES student (id),

  CONSTRAINT student_subject_subject_schedule_id_fk FOREIGN KEY (subject_schedule_id)
    REFERENCES subject_schedule (id)
);
