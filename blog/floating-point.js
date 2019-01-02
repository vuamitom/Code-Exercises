// assuming BigEndian
/**
 * getting bit sequence of an input number
 */
function toBits(n, bitCount) {
	var x = n;
	var bs = [];
	for (var b = 0; b < bitCount; b++) {
		x = n >> b;		
		bs.push(x & 0x01);
	}
	return bs.reverse();
}

/**
 * nicely print a binary number. omit trailing 0 after the dot.
 */
function toBinaryStr(bits) {	
	var suffix = bits.slice(1).join('').replace(/0+$/, '');
	suffix = suffix.length == 0? '0': suffix;
	return bits[0] + '.' + suffix;
}

function toMathString(n) {
	var buffer = new ArrayBuffer(4);
	new DataView(buffer).setFloat32(0, n);
	var bytes = new Uint8Array(buffer);

	// 0 - positive, 1 - negative
	var sign = (bytes[0] >> 7) > 0 ? '-': '';
	var exp = (bytes[0] << 1) | (bytes[1] >> 7);
	// expected: 126 , in binary 01111110
	// for float32, minus 127 from raw bits to get signed value
	var expVal = exp - 127;
	// expected: -1
	var expSign = expVal > 0? '': '-';


	// the most significant bit is 1 and is ommited
	// So we put it back here
	var sig = (((bytes[1] & 0x7F) | 0x80) << 16) | (bytes[2] << 8) | bytes[3];

	// expected: 8388608 , which is 10...0 (23 zeros)
	var mathRep = toBinaryStr(toBits(sig, 24)) + 'E' 
			+ expSign 
			+ toBits(Math.abs(expVal), 8).join('').replace(/^0+/,'');
	return mathRep;
}