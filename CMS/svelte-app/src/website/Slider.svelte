<script>
    import 'tw-elements';
    import {Net} from "../net";

    export let sliderData;
</script>

<div style="margin-top:100px" id="carouselExampleCaptions" class="carousel slide relative" data-bs-ride="carousel">
    <div class="carousel-indicators absolute right-0 bottom-0 left-0 flex justify-center p-0 mb-4">
        {#each sliderData.slides as slide, i}
            {#if i === 0}
                <button
                        type="button"
                        data-bs-target="#carouselExampleCaptions"
                        data-bs-slide-to="0"
                        class="active"
                        aria-current="true"
                        aria-label="Slide 1"
                ></button>
            {:else}
                <button
                        type="button"
                        data-bs-target="#carouselExampleCaptions"
                        data-bs-slide-to="{i}"
                        aria-label="Slide {i+1}"
                ></button>
            {/if}
        {/each}
    </div>

    <div  style="display:flex; justify-content:center;" class="carousel-inner relative w-full overflow-hidden">

        {#each sliderData.slides as slide, i}
            <div class="carousel-item {i===0?'active':''} relative float-left w-full">
                {#await Net.fetchPhoto(slide.src)}
                    Loading photo...
                {:then photo}
                    <img
                            src="{photo}"
                            class="block w-full"
                            alt="SLIDE: {i} SRC={photo}"
                    />
                {/await}
                <div class="carousel-caption hidden md:block absolute text-center maBycJakosZaciemnione">
                    <h5 class="text-xl">{slide.title}</h5>
                    <p>{slide.description}</p>
                </div>
            </div>
        {/each}
    </div>
    <button
            class="carousel-control-prev absolute top-0 bottom-0 flex items-center justify-center p-0 text-center border-0 hover:outline-none hover:no-underline focus:outline-none focus:no-underline left-0"
            type="button"
            data-bs-target="#carouselExampleCaptions"
            data-bs-slide="prev"
    >
        <span class="carousel-control-prev-icon inline-block bg-no-repeat" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
    </button>
    <button
            class="carousel-control-next absolute top-0 bottom-0 flex items-center justify-center p-0 text-center border-0 hover:outline-none hover:no-underline focus:outline-none focus:no-underline right-0"
            type="button"
            data-bs-target="#carouselExampleCaptions"
            data-bs-slide="next"
    >
        <span class="carousel-control-next-icon inline-block bg-no-repeat" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
    </button>
</div>

<style>
    img {
        height: 500px;
        object-fit: cover;
    }
    .carousel-inner{/*
    flex-direction:column;
    align-items:center;
    */}

    a:visited{
    text-decoration: none;
    color:black;
}
</style>