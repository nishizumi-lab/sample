import 'dart:collection';

class DC {
  DC() {}

  // 西暦 → 和暦
  String calcResistor(num current, num voltage, String currentUnit, String voltageUnit) {

    if (currentUnit == "kA") {
      current = current * 0.001;
    } else if (currentUnit == "mA") {
      current = current * 1000;
    } else if (currentUnit == "μA") {
      current = current * 1000000;
    }

    if (currentUnit == "kA") {
      current = current * 0.001;
    } else if (currentUnit == "mA") {
      current = current * 1000;
    } else if (currentUnit == "μA") {
      current = current * 1000000;
    }
    
    return wareki;
  }

}

// 検証用
void main() {
  var calender = Calendar();

  // 西暦 -> 中陰
  var chuinMap = calender.yearToChuin(DateTime.now());

  for (var chuin in chuinMap.entries) {
    print(chuin.key);
    print(chuin.value);
  }

  // 西暦 -> 年回
  var nenkaiMap = calender.yearToNenkai(DateTime.now());

  for (var nenkai in nenkaiMap.entries) {
    print(nenkai.key);
    print(nenkai.value);
  }
}
