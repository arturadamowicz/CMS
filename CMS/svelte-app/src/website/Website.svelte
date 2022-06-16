<script>
    import Header from './Header.svelte';
    import Slider from "./Slider.svelte";
    import News from "./News.svelte";
    import Footer from "./Footer.svelte";

    const data_json = (async () => {
        const response = await fetch('http://127.0.0.1:5000/data')
        const json =  await response.json()
        console.log(json)
        return json
    })()

</script>

{#await data_json}
    Loading...
{:then data}
    <Header headerData={data.header}/>
    <Slider sliderData={data.content.slider}></Slider>
    <News newsData={data.content.news}></News>
    <Footer footerData={data.footer}></Footer>
{/await}

<style>
a:visited{
    text-decoration: none;
    color:black;
}
</style>