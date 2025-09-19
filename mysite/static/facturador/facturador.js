/* Shivving (IE8 is not supported, but at least it won't look as awful)
/* ========================================================================== */




(function (document) {
	var
		head = document.head = document.getElementsByTagName('head')[0] || document.documentElement,
		elements = 'article aside audio bdi canvas data datalist details figcaption figure footer header hgroup mark meter nav output picture progress section summary time video x'.split(' '),
		elementsLength = elements.length,
		elementsIndex = 0,
		element;

	while (elementsIndex < elementsLength) {
		element = document.createElement(elements[++elementsIndex]);
	}

	element.innerHTML = 'x<style>' +
		'article,aside,details,figcaption,figure,footer,header,hgroup,nav,section{display:block}' +
		'audio[controls],canvas,video{display:inline-block}' +
		'[hidden],audio{display:none}' +
		'mark{background:#FF0;color:#000}' +
		'</style>';


	return head.insertBefore(element.lastChild, head.firstChild);
})(document);

/* Prototyping
/* ========================================================================== */

(function (window, ElementPrototype, ArrayPrototype, polyfill) {
	function NodeList() { [polyfill] }
	NodeList.prototype.length = ArrayPrototype.length;

	ElementPrototype.matchesSelector = ElementPrototype.matchesSelector ||
		ElementPrototype.mozMatchesSelector ||
		ElementPrototype.msMatchesSelector ||
		ElementPrototype.oMatchesSelector ||
		ElementPrototype.webkitMatchesSelector ||
		function matchesSelector(selector) {
			return ArrayPrototype.indexOf.call(this.parentNode.querySelectorAll(selector), this) > -1;
		};

	ElementPrototype.ancestorQuerySelectorAll = ElementPrototype.ancestorQuerySelectorAll ||
		ElementPrototype.mozAncestorQuerySelectorAll ||
		ElementPrototype.msAncestorQuerySelectorAll ||
		ElementPrototype.oAncestorQuerySelectorAll ||
		ElementPrototype.webkitAncestorQuerySelectorAll ||
		function ancestorQuerySelectorAll(selector) {
			for (var cite = this, newNodeList = new NodeList; cite = cite.parentElement;) {
				if (cite.matchesSelector(selector)) ArrayPrototype.push.call(newNodeList, cite);
			}

			return newNodeList;
		};

	ElementPrototype.ancestorQuerySelector = ElementPrototype.ancestorQuerySelector ||
		ElementPrototype.mozAncestorQuerySelector ||
		ElementPrototype.msAncestorQuerySelector ||
		ElementPrototype.oAncestorQuerySelector ||
		ElementPrototype.webkitAncestorQuerySelector ||
		function ancestorQuerySelector(selector) {
			return this.ancestorQuerySelectorAll(selector)[0] || null;
		};
})(this, Element.prototype, Array.prototype);

/* Helper Functions
/* ========================================================================== */

function generateTableRow(nombre, cantidad, precio) {
	var emptyColumn = document.createElement('tr');

	emptyColumn.innerHTML = `<td><a class="cut">-</a><span${nombre}></span></td>` +
		`<td><span>${cantidad}</span></td>` +
		`<td><span data-prefix>$</span><span>${precio}</span></td>`
	return emptyColumn;
}

function parseFloatHTML(element) {
	return parseFloat(element.innerHTML.replace(/[^\d\.\-]+/g, '')) || 0;
}

function parsePrice(number) {
	return number.toFixed(2).replace(/(\d)(?=(\d\d\d)+([^\d]|$))/g, '$1,');
}

/* Update Number
/* ========================================================================== */

function updateNumber(e) {

	var
		activeElement = document.activeElement,
		value = parseFloat(activeElement.innerHTML),
		wasPrice = activeElement.innerHTML == parsePrice(parseFloatHTML(activeElement));

	if (!isNaN(value) && (e.keyCode == 38 || e.keyCode == 40 || e.wheelDeltaY)) {
		e.preventDefault();

		value += e.keyCode == 38 ? 1 : e.keyCode == 40 ? -1 : Math.round(e.wheelDelta * 0.025);
		value = Math.max(value, 0);

		activeElement.innerHTML = wasPrice ? parsePrice(value) : value;
	}

	updateInvoice();
}

/* Update Invoice
/* ========================================================================== */

function updateInvoice() {
	var total = 0;
	var cells, price, total, a, i;

	// update inventory cells
	// ======================

	for (var a = document.querySelectorAll('table.inventory tbody tr'), i = 0; a[i]; ++i) {
		// get inventory row cells
		cells = a[i].querySelectorAll('span:last-child');

		// set price as cell[2] * cell[3]
		price = parseFloatHTML(cells[1]) * parseFloatHTML(cells[2]);

		// add price to total
		total += price;

		// set row total
		cells[3].innerHTML = price;
	}

	// update balance cells
	// ====================

	// get balance cells
	cells = document.querySelectorAll('table.balance td:last-child span:last-child');

	// set total
	cells[0].innerHTML = total;

	// set balance and meta balance
	cells[2].innerHTML = document.querySelector('table.meta tr:last-child td:last-child span:last-child').innerHTML = parsePrice(total - parseFloatHTML(cells[1]));

	// update prefix formatting
	// ========================

	var prefix = document.querySelector('#prefix').innerHTML;
	for (a = document.querySelectorAll('[data-prefix]'), i = 0; a[i]; ++i) a[i].innerHTML = prefix;

	// update price formatting
	// =======================

	for (a = document.querySelectorAll('span[data-prefix] + span'), i = 0; a[i]; ++i) if (document.activeElement != a[i]) a[i].innerHTML = parsePrice(parseFloatHTML(a[i]));
}

/* On Content Load
/* ========================================================================== */

function onContentLoad() {
	var
		input = document.querySelector('input'),
		image = document.querySelector('img');

	function onClick(e) {
		var element = e.target.querySelector('[contenteditable]'), row;

		element && e.target != document.documentElement && e.target != document.body && element.focus();

		if (e.target.matchesSelector('.seleccionar-btn')) {
			document.querySelector('tabla-inventory tbody-inventory').appendChild(generateTableRow(nombre, cantidad, precio));
		}
		else if (e.target.className == 'cut') {
			row = e.target.ancestorQuerySelector('tr');

			row.parentNode.removeChild(row);
			CalcularFactura()
		}

		//updateInvoice();
	}

	function onEnterCancel(e) {
		e.preventDefault();

		image.classList.add('hover');
	}

	function onLeaveCancel(e) {
		e.preventDefault();

		image.classList.remove('hover');
	}

	function onFileInput(e) {
		image.classList.remove('hover');

		var
			reader = new FileReader(),
			files = e.dataTransfer ? e.dataTransfer.files : e.target.files,
			i = 0;

		reader.onload = onFileLoad;

		while (files[i]) reader.readAsDataURL(files[i++]);
	}

	function onFileLoad(e) {
		var data = e.target.result;

		image.src = data;
	}

	function inputCantidad(event) {
		if (event.target.matches("td[contenteditable]")) {
			let contenido = event.target.textContent;

			// Filtra solo números y un único punto decimal
			contenido = contenido.replace(/[^0-9.]/g, '');

			// Limita a un solo punto decimal y solo permite 3 decimales después de él
			const partes = contenido.split('.');
			if (partes.length > 2) {
				contenido = partes[0] + '.' + partes.slice(1).join('');
			} else if (partes.length === 2) {
				partes[1] = partes[1].substring(0, 3); // Limita los decimales a 3 dígitos
				contenido = partes.join('.');
			}

			// Usamos setTimeout para evitar la interrupción del cursor
			setTimeout(() => {
				event.target.textContent = contenido;

				// Restaurar el cursor al final
				const range = document.createRange();
				const selection = window.getSelection();

				range.selectNodeContents(event.target);
				range.collapse(false);
				selection.removeAllRanges();
				selection.addRange(range);
			}, 0);
		}
	}

	if (window.addEventListener) {
		//document.addEventListener('click', onClick);

		document.addEventListener('input', inputCantidad);

		//document.addEventListener('mousewheel', updateNumber);
		//document.addEventListener('keydown', updateNumber);

		//document.addEventListener('keydown', updateInvoice);
		//document.addEventListener('keyup', updateInvoice);

		input.addEventListener('focus', onEnterCancel);
		input.addEventListener('mouseover', onEnterCancel);
		input.addEventListener('dragover', onEnterCancel);
		input.addEventListener('dragenter', onEnterCancel);

		input.addEventListener('blur', onLeaveCancel);
		input.addEventListener('dragleave', onLeaveCancel);
		input.addEventListener('mouseout', onLeaveCancel);

		input.addEventListener('drop', onFileInput);
		input.addEventListener('change', onFileInput);
	}
}

window.addEventListener && document.addEventListener('DOMContentLoaded', onContentLoad);



//					Funciones adicionales propias
// =====================================================================

let celdaActual = null;

// Función para abrir el modal de busqueda de Clientes
function abrirModal() {
	document.getElementById("miModal").style.display = "block";
}

function cerrarModal() {
	document.getElementById("miModal").style.display = "none";
}

// Función para abrir y cerrar el modal de busqueda de Productos
function abrirModalP() {
	document.getElementById("miModalP").style.display = "block";
	document.getElementById("busquedaP").value = ''
	var tabla = document.getElementById("tablap").getElementsByTagName('tbody')[0];
	tabla.innerHTML = "";

}

function cerrarModalP() {
	document.getElementById("miModalP").style.display = "none";
}


/* Funciones para abrir el modal de cantidad y modificar cantidad */

function abrirModalCant(celda) {
	celdaActual = celda;
	var valor = celda.querySelector("span").innerText;
	document.getElementById("input-cantidad").value = valor;
	document.getElementById("modalcantidad").style.display = "flex";
}

document.getElementById("bt-fin-cant").onclick = function () {
	var fila = celdaActual.parentNode.parentNode;
	var nuevoValor = document.getElementById("input-cantidad").value;

	if (celdaActual) {
		celdaActual.querySelector("span").innerText = nuevoValor;
	}
	var precioUn = parseFloat(fila.cells[2].querySelectorAll("span")[1].innerText);
	var total = redondearDecimales(parseFloat(precioUn * nuevoValor), 2)
	fila.cells[3].querySelectorAll("span")[1].innerText = total

	CalcularFactura()
	document.getElementById("modalcantidad").style.display = "none";
};

function abrirModalPres(celda) {
	celdaActual = celda;
	var valor = celda.querySelector("span").innerText;
	document.getElementById("input-precio").value = valor;
	document.getElementById("modalprecio").style.display = "flex";
}

document.getElementById("bt-fin-precio").onclick = function () {
	var fila = celdaActual.parentNode.parentNode;
	var nuevoValor = document.getElementById("input-precio").value;

	if (celdaActual) {
		celdaActual.querySelectorAll("span")[1].innerText = nuevoValor;
	}
	var precioUn = parseFloat(fila.cells[2].querySelectorAll("span")[1].innerText);
	var total = redondearDecimales(parseFloat(precioUn * nuevoValor), 2)
	fila.cells[3].querySelectorAll("span")[1].innerText = total

	CalcularFactura()
	document.getElementById("modalprecio").style.display = "none";
};



/* Llamadas AJAX, busqueda de productos, clientes y seleccion de fila para el facturador */
function buscarClientes() {
	var query = document.getElementById("busqueda").value;  // Obtener valor ingresado
	var tabla = document.getElementById("tabla").getElementsByTagName('tbody')[0];

	// Evitar consultas vacías
	if (query.length < 1) {
		tabla.innerHTML = "";  // Vaciar tabla si el campo está vacío
		return;
	}

	// Realizar petición AJAX
	fetch(`/buscar_clientes?q=${query}`)
		.then(response => response.json())
		.then(data => {
			tabla.innerHTML = "";
			// Insertar los nuevos resultados en la tabla
			data.clientes.forEach(cliente => {
				var nuevaFila = tabla.insertRow();
				var celdaCUIT = nuevaFila.insertCell(0);
				var celdaRazons = nuevaFila.insertCell(1);
				var celdaAccion = nuevaFila.insertCell(2);
				celdaCUIT.innerHTML = `<td>${cliente.cuit}</td>`;
				celdaRazons.innerHTML = `<td>${cliente.razons}</td>`;
				celdaAccion.innerHTML = `<td><button class="seleccionar-btn" onclick="seleccionarFila(this)">Seleccionar</button></td>`;
			});
		});
}

function buscarProductos() {
	var query = document.getElementById("busquedaP").value;  // Obtener valor ingresado
	var query2 = document.getElementById("list").innerText;
	var tabla = document.getElementById("tablap").getElementsByTagName('tbody')[0];

	// Evitar consultas vacías
	if (query.length < 1) {
		tabla.innerHTML = "";  // Vaciar tabla si el campo está vacío
		return;
	}

	// Realizar petición AJAX
	fetch(`/buscar_productos?q=${query}&w=${query2}`)
		.then(response => response.json())
		.then(data => {
			tabla.innerHTML = "";
			// Insertar los nuevos resultados en la tabla
			data.productos.forEach(producto => {
				var nuevaFila = tabla.insertRow();
				var celdaNombre = nuevaFila.insertCell(0);
				var celdaCant = nuevaFila.insertCell(1);
				var celdaPrecio = nuevaFila.insertCell(2);
				var celdaAccion = nuevaFila.insertCell(3);
				celdaNombre.innerHTML = `<td>${producto.nombre}</td>`;
				celdaCant.textContent = "1"; // Establecer el texto inicial
				celdaCant.setAttribute("contenteditable", "true"); // Hacer editable
				celdaCant.setAttribute("onclick", "borrarContenido(this)")
				celdaPrecio.innerHTML = `<td>${producto.precio}</td>`;
				celdaAccion.innerHTML = `<td><button class="seleccionar-btn" onclick="seleccionarFilaP(this)">Seleccionar</button></td>`;
			});
		});
}

function seleccionarFila(boton) {
	// Obtener la fila que contiene el botón
	var cuit = boton.parentNode.parentNode.cells[0].innerText;

	// Llamada AJAX a Django para procesar los datos
	fetch(`/seleccionar_cliente?q=${cuit}`)
		.then(response => response.json())
		.then(data => {
			document.getElementById("razons").innerText = `${data.dato_cli[0].razons}`;
			document.getElementById("cuit").innerText = `${data.dato_cli[0].cuit}`;
			document.getElementById("dir").innerText = `${data.dato_cli[0].direccion}`;
			document.getElementById("resp").innerText = `${data.dato_cli[0].responsabilidad_id}`;
			document.getElementById("list").innerText = `${data.dato_cli[0].lista}`;
			document.getElementById("BCliente").disabled = true;
			document.getElementById("BProductos").disabled = false;
		})
		.catch(error => console.error("Error en la solicitud:", error));

	document.getElementById("miModal").style.display = "none";
}

function seleccionarFilaP(boton) {
	// Obtener la fila que contiene el botón
	var nombre = boton.parentNode.parentNode.cells[0].innerText;
	var cantidad = boton.parentNode.parentNode.cells[1].innerText;
	var precio = boton.parentNode.parentNode.cells[2].innerText;

	precio = precio / 1.21

	tabla = document.getElementById("tabla-inventory").getElementsByTagName('tbody')[0];

	var nuevaFila = tabla.insertRow();
	var celdaDesc = nuevaFila.insertCell(0);
	var celdaCant = nuevaFila.insertCell(1);
	var celdaPrice = nuevaFila.insertCell(2);
	var celdaPrice2 = nuevaFila.insertCell(3);
	var aux = parseFloat(cantidad) * parseFloat(precio)
	celdaDesc.innerHTML = `<td><a class="cut">-</a><span>${nombre}</span></td>`;
	celdaCant.innerHTML = `
	<td>
		<div class="celda-cantidad">
		<span class="cantidad-texto">${cantidad}</span>
		<button class="btn-cantidad" onclick="abrirModalCant(this.parentNode)">✏️</button>
		</div>
	</td>
	`;
	celdaPrice.innerHTML = `
	<td>
		<div class="celda-cantidad">
		<span class="cantidad-texto">${redondearDecimales(precio, 4)}</span>
		<button class="btn-cantidad" onclick="abrirModalPres(this.parentNode)">✏️</button>
		</div>
	</td>
	`;
	
	//celdaPrice.innerHTML = `<td><span data-prefix>$</span><span>${redondearDecimales(precio, 4)}</span></td>`;
	celdaPrice2.innerHTML = `<td><span data-prefix>$</span><span>${redondearDecimales(aux, 2)}</span></td>`;

	boton.parentNode.parentNode.remove()

	CalcularFactura()
}




/* Funciones de utilidad */

function redondearDecimales(numero, decimales) {
	numeroRegexp = new RegExp('\\d\\.(\\d){' + decimales + ',}');   // Expresion regular para numeros con un cierto numero de decimales o mas
	if (numeroRegexp.test(numero)) {         // Ya que el numero tiene el numero de decimales requeridos o mas, se realiza el redondeo
		return Number(numero.toFixed(decimales));
	} else {
		return Number(numero.toFixed(decimales)) === 0 ? 0 : numero;  // En valores muy bajos, se comprueba si el numero es 0 (con el redondeo deseado), si no lo es se devuelve el numero otra vez.
	}
}

function CalcularFactura() {
	var tabla = document.getElementById("tbody-inventory")
	var total = 0

	for (let i = 0; i < tabla.rows.length; i++) {
		let fila = tabla.rows[i]
		let celda = fila.cells[3].querySelectorAll("span")[1].innerText
		total += parseFloat(celda)
	}
	var total2 = total * 1.21

	document.getElementById('subtotalSpan').innerHTML = `$ ${redondearDecimales(total, 2)}`

	var iva = (total * 0.21) / 1.21
	document.getElementById('ivaSpan').innerHTML = `$ ${redondearDecimales(iva, 2)}`

	document.getElementById('totalSpan').innerHTML = `$ ${redondearDecimales(total2, 2)}`
	document.getElementById('totalSpan2').innerHTML = `$ ${redondearDecimales(total2, 2)}`
}

function borrarContenido(celda) {
	celda.innerText = ""; // Borra el contenido de la celda
}

