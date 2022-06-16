export class Net {
    static fetchPhoto(path) {
        return (async () => {
            const response = await fetch('http://127.0.0.1:5000/gfx?name=' + path,
                // {
                // method:"POST",
                // body:{name:path},
                // headers:{'Content-Type':"application/json"}
                // }
            )
            const blob = await response.blob()
            const createdURL = URL.createObjectURL(blob)
            console.log(createdURL)
            return createdURL
        })()
    }

    static sendPhoto(src, file) {
        const blob = new Blob([file], {
            type: "application/octet-stream"
        });

        let data = new FormData()
        data.append('file', blob, "file")

        alert()
        let res = fetch('http://127.0.0.1:5000/gfx/insert?name=' + src, {
            method: "POST",
            body: data
        })
        return res
    }
}

export class FormNet {
    static json = {
        header: {},
        content: {
            slider: {},
            news: {}
        },
        footer: {}
    };
    static header;
    static news;
    static slider;
    static footer;


    static updateData() {
        // this.json.header = this.header
        this.json.content.slider.slides = this.slider
        this.json.content.news = this.news
        // this.json.footer = this.footer
        console.log(this.json)

        const str = JSON.stringify(this.json);
        const bytes = new TextEncoder().encode(str);
        const blob = new Blob([bytes], {
            type: "application/json;charset=utf-8"
        });


        let data = new FormData()
        data.append('file', blob, "file")


        fetch('http://127.0.0.1:5000/data/update', {
            method: "POST",
            body: data,
            // headers:{"Content-Type":"application/octet-stream"}
        })
    }
}