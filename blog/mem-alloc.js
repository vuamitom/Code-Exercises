function time(fn, iter) {
    let s = new Date().getTime();
    for (let i = 0; i < iter; i++) {
        fn();
    }
    let dur = new Date().getTime() - s;
    return dur;
}

function fixSizeArray() {
    let iter = 10000,
        size = 100000,
        dur;
    dur = time(() => {
        let ar = [];
        for (let s = 0; s < size; s++)
            ar.push(s);
    }, iter);
    console.log(`pushing into array takes ${dur}ms`);

    dur = time(() => {
        let ar = new Array(size);
        for (let s = 0; s < size; s++)
            ar[s] = s;
    }, iter);

    console.log(`pre-allocate array takes ${dur}ms`);
}

function mapVsForeach() {
    let iter = 10000,
        ar = new Array(100000),
        dur;
    dur = time(() => {
        ar.map(a => a)
    }, iter);
    console.log(`using 'map' takes ${dur}ms`);

    dur = time(() => {
        ar.forEach(a => a)
    }, iter);

    console.log(`using 'forEach' takes ${dur}ms`);
}

function stringConcatenate() {
    let iter = 1000,
        size = 10000,
        dur;
    

    dur = time(() => {
        // ar.forEach(a => a)
        let a = new Array(size);
        for (let i = 0; i < size; i++)
            a[i] = 'a'
        a = a.join('');
        return a;
    }, iter);

    console.log(`using [].join takes ${dur}ms`);   

    dur = time(() => {
        let a = '';
        for (let i = 0; i < size; i++)
            a += 'a';
        return a;
    }, iter);
    console.log(`using '+' on string takes ${dur}ms`);
}

stringConcatenate();