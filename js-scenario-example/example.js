function getCookie(name) {
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}
function setCookie(name, value, options = {}) {

  options = {
    path: '/',
    // при необходимости добавьте другие значения по умолчанию
    ...options
  };

  if (options.expires instanceof Date) {
    options.expires = options.expires.toUTCString();
  }

  let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);

  for (let optionKey in options) {
    updatedCookie += "; " + optionKey;
    let optionValue = options[optionKey];
    if (optionValue !== true) {
      updatedCookie += "=" + optionValue;
    }
  }

  document.cookie = updatedCookie;
}


function popUpMessage(text, fromElement, toSide, withClickAskElement) {
    alert(text+" Окно появилось у "+fromElement+" элемента со стороны "+toSide+" и после нажатия далее, попросит нажать на " + withClickAskElement+" элемент.");
}


function getScenarioPositionName() {
    a = getCookie("scenario_position_name")
    return a
}
a = getScenarioPositionName()
alert(a)
if (!a || a == undefined) {
    a = "start"
    setCookie("scenario_position_name", a)
}
if (a == "start") {
    popUpMessage("Привет, АНДРЕЙ!\n Не хочешь принять участие в соревновании?", document.getElementsByTagName("a"), 'top-left', 10)
}