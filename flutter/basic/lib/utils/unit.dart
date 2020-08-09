import 'dart:collection';

class Unit {
  Unit() {}

  // 西暦 → 和暦
  double convert(double srcValue, String srcUnit, String dstUnit) {

    double dstValue = 0.0;

    // μ　→　other
    if (srcUnit == "μ" && dstUnit == "m") {
      dstValue = srcValue * 0.001;
    } else if (srcUnit == "μ" && dstUnit == "SI") {
      dstValue = srcValue * 0.000001;
    } else if (srcUnit == "μ" && dstUnit == "k") {
      dstValue = srcValue * 0.000000001;
    } else if (srcUnit == "μ" && dstUnit == "M") {
      dstValue = srcValue * 0.000000000001;
    } else if (srcUnit == "μ" && dstUnit == "G") {
      dstValue = srcValue * 0.000000000000001;
    // m　→　other
    } else if (srcUnit == "m" && dstUnit == "μ") {
      dstValue = srcValue * 1000;
    } else if (srcUnit == "m" && dstUnit == "SI") {
      dstValue = srcValue * 0.001;
    } else if (srcUnit == "m" && dstUnit == "k") {
      dstValue = srcValue * 0.000001;
    } else if (srcUnit == "m" && dstUnit == "M") {
      dstValue = srcValue * 0.000000001;
    } else if (srcUnit == "m" && dstUnit == "G") {
      dstValue = srcValue * 0.000000000001;
    // SI　→　other
    } else if (srcUnit == "SI" && dstUnit == "μ") {
      dstValue = srcValue * 1000000;
    } else if (srcUnit == "SI" && dstUnit == "m") {
      dstValue = srcValue * 1000;
    } else if (srcUnit == "SI" && dstUnit == "k") {
      dstValue = srcValue * 0.001;
    } else if (srcUnit == "SI" && dstUnit == "M") {
      dstValue = srcValue * 0.000001;
    } else if (srcUnit == "SI" && dstUnit == "G") {
      dstValue = srcValue * 0.000000001;
    // k → other
    } else if (srcUnit == "k" && dstUnit == "μ") {
      dstValue = srcValue * 1000000000;
    } else if (srcUnit == "k" && dstUnit == "m") {
      dstValue = srcValue * 1000000;
    } else if (srcUnit == "k" && dstUnit == "SI") {
      dstValue = srcValue * 1000;
    } else if (srcUnit == "k" && dstUnit == "M") {
      dstValue = srcValue * 0.001;
    } else if (srcUnit == "k" && dstUnit == "G") {
      dstValue = srcValue * 0.000001;
    // M → other
    } else if (srcUnit == "M" && dstUnit == "μ") {
      dstValue = srcValue * 1000000000000;
    } else if (srcUnit == "M" && dstUnit == "m") {
      dstValue = srcValue * 1000000000;
    } else if (srcUnit == "M" && dstUnit == "SI") {
      dstValue = srcValue * 1000000;
    } else if (srcUnit == "M" && dstUnit == "k") {
      dstValue = srcValue * 0.001;
    } else if (srcUnit == "M" && dstUnit == "G") {
      dstValue = srcValue * 0.000001;
    // G → other
    } else if (srcUnit == "G" && dstUnit == "μ") {
      dstValue = srcValue * 1000000000000000;
    } else if (srcUnit == "G" && dstUnit == "m") {
      dstValue = srcValue * 1000000000000;
    } else if (srcUnit == "G" && dstUnit == "SI") {
      dstValue = srcValue * 1000000000;
    } else if (srcUnit == "G" && dstUnit == "k") {
      dstValue = srcValue * 1000000;
    } else if (srcUnit == "G" && dstUnit == "M") {
      dstValue = srcValue * 1000;
      // else(SI -> SI)
    } else{
      dstValue = srcValue;
    }

    
    return dstValue;
  }

}

// 検証用
void main() {
  var unit = Unit();

  // μ -> SI
  var dst1 = unit.convert(5, "μ", "SI");
  print(dst1); // 0.0000049999999999999996

  // k -> G
  var dst2 = unit.convert(5, "k", "M");
  print(dst2); // 0.005

  // else
  var dst3 = unit.convert(5, "A", "SI");
  print(dst3); // 5.0
}
