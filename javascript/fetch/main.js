
url = 'https://raw.githubusercontent.com/nishizumi-lab/sample/master/application/readme.md';

    const getCode = (url) => {
        return new Promise((a, b) => {
            const promise = fetch(url);
            const code = promise.then(text => text.text()).then(code => a(code)).cache(err => b(new Error(err)));
        });
    };

