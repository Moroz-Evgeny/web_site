document.addEventListener('DOMContentLoaded', function () {
	const hamburger = document.querySelector('.hamburger')
	const sidebar = document.querySelector('.sidebar')

	hamburger.addEventListener('click', function () {
		sidebar.classList.toggle('active') // Переключаем класс active для бокового меню
		hamburger.classList.toggle('active') // Переключаем класс active для гамбургера
	})

	// Скрыть меню при изменении размера окна
	window.addEventListener('resize', function () {
		if (window.innerWidth > 860) {
			sidebar.classList.remove('active') // Убираем класс active при увеличении окна
			hamburger.classList.remove('active') // Убираем класс active у гамбургера
		}
	})

	// Закрытие сайдбара при клике вне его области
	document.addEventListener('click', function (event) {
		if (
			sidebar.classList.contains('active') &&
			!sidebar.contains(event.target) &&
			!hamburger.contains(event.target)
		) {
			sidebar.classList.remove('active') // Закрыть сайдбар
			hamburger.classList.remove('active') // Вернуть гамбургер в исходное состояние
		}
	})
})
function hidePlaceholder() {
	const searchInput = document.querySelector('.search-input')
	searchInput.placeholder = '' // Убираем текст плейсхолдера
}

function showPlaceholder() {
	const searchInput = document.querySelector('.search-input')
	if (searchInput.value === '') {
		searchInput.placeholder = 'Поиск по статьям...' // Возвращаем текст плейсхолдера
	}
}




