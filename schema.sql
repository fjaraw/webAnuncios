drop table if exists entries;

--tabla de anuncios

create table entry (
  id integer primary key autoincrement,
  title text not null,
  description text not null,
	ubicacion text not null,
  image text,
	tag text not null,
	fk_id_user text,
	FOREIGN KEY (fk_id_user) REFERENCES user (user)
);

--tabla de usuarios

create table user (
  ids integer primary key autoincrement,
  name text not null,
  user text not null unique,
  pass text not null,
	dir text not null,
	tel text not null,
	mail text not null
);

--poblar tabla de anuncios

insert into entry (title, description, ubicacion, image, tag, fk_id_user) values ("Arriendo Casa", "Casa con dos dormitorios, un baño, cocina americana.","Valdivia", "1.jpg", "a","admin");
insert into entry (title, description, ubicacion, image, tag, fk_id_user) values ("Venta Casa", "Increíble oportunidad: 5 dormitorios, 3 baños, aplio espacio, entrada de vehiculo.","Osorno", "2.jpg", "v","jperez");
insert into entry (title, description, ubicacion, image, tag, fk_id_user) values ("Venta lujosa Propiedad", "Se vende moderna casa: cuenta con 2 dormitorios, dos baños, vista privilegiada, piscina y terraza.","Santiago", "3.jpg", "v","franvi");
insert into entry (title, description, ubicacion, image, tag, fk_id_user) values ("Arriendo propiedad", "Dos dormitorios, un baños, cocina americana.","Valdivia", "4.jpg", "a","dimu");
insert into entry (title, description, ubicacion, image, tag, fk_id_user) values ("Volkswagen Beetle 2014", "Color rojo, Mecanico, Velocidad Crucero, Alarma, Cierre a Distancia, Llantas, doble Airbag, A/C, Sello Verde. Valor: $3.900.000","Valdivia", "5.jpg", "v","pedro189");
insert into entry (title, description, ubicacion, image, tag, fk_id_user) values ("Ford mustang GT", "Año 2010 color amarillo, deportivo, capot fibra de carbono. $17.980.00","Santiago", "6.jpg", "v","alejo");
insert into entry (title, description, ubicacion, image, tag, fk_id_user) values ("CHEVROLET CRUZE", "Es deportivo, llamativo y está más que listo para salir a la calle. Desde $8.890.000.","Temuco", "7.jpg", "v","admin");
insert into entry (title, description, ubicacion, image, tag, fk_id_user) values ("Mercedes SLS AMG", "Diseño SLS AMG “Gullwing”, alcanza los 317 Km/h de velocidad máxima y los 100 Km/h desde parado en tan sólo 3.8 segundos. Valor desde $143.900.000","Santiago", "8.jpg", "v","franvi");
insert into entry (title, description, ubicacion, image, tag, fk_id_user) values ("Ron Damon", "No te doy otra no mas...","Chile", "9.jpg", "s","dimu");
insert into entry (title, description, ubicacion, image, tag, fk_id_user) values ("Copa del mundo 2014", "La Copa Mundial de la FIFA Brasil 2014 será la XX edición de la Copa Mundial de Fútbol. Esta versión del torneo se realizará en Brasil entre el 12 de junio y el 13 de julio de 2014.","Brasil", "10.jpg", "s","pedro189");
insert into entry (title, description, ubicacion, image, tag, fk_id_user) values ("Lollapalooza Chile 2014", "Red Hot Chili Peppers, Nine Inch Nails y Phoenix protagonizarán la primera jornada de Lollapalooza Chile 2014, mientras que Soundgarden, Arcade Fire y Pixies serán los encargados de cerrar el festival, que se celebrará el 29 y 30 de marzo en el Parque O’Higgins.","Santiago", "11.jpg", "s","admin");
insert into entry (title, description, ubicacion, image, tag, fk_id_user) values ("Bierfest Kunstmann 2014", "Entre el 30 de enero y el 2 de febrero se realizará una nueva versión de la Bierfest Kunstmann 2014 en Valdivia.","Valdivia", "12.jpg", "s","jperez");

--poblar datos de usuarios

insert into user (name, user, pass, dir, tel, mail) values ("Administrador", "admin", "1234","Los robles 123", "12345678", "admin@admin.com");
insert into user (name, user, pass, dir, tel, mail) values ("Juanito Perez", "jperez", "12345", "Picarte 123", "76542321", "jperez@gmail.com");
insert into user (name, user, pass, dir, tel, mail) values ("Pedro Reyes", "pedro189", "pere189","Los aromos 2350", "78392245", "pedro_189@hotmail.com");
insert into user (name, user, pass, dir, tel, mail) values ("Diego Muñoz", "dimu", "dimu123", "Los avellanos 149", "99391234", "diego@live.cl");
insert into user (name, user, pass, dir, tel, mail) values ("Francisco villar", "franvi", "asdfg","Avda. Argentina 407", "83294123", "fvillar@hotmail.com");
insert into user (name, user, pass, dir, tel, mail) values ("Alejandro Magno", "alejo", "ale123", "Macedonia 336", "63451237", "alemagno@gmail.com");
