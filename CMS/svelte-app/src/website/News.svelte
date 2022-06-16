<script>

    export let newsData;
</script>

<div class = "flex flex-wrap justify-center margin">
    {#each newsData as news}

        <div class="flex justify-center w-3/12">
            <div style="margin-bottom:60px" class="block p-6 rounded-lg shadow-lg bg-white max-w-sm">
                <h5 class="text-gray-900 text-xl leading-tight font-medium mb-2">{news.title}</h5>
                <p class="text-gray-700 text-base mb-4">
                    {news.content}
                </p>
                <a href={news.href} type="button" class=" inline-block px-6 py-2.5 bg-blue-600 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out">Read more</a>
            </div>
        </div>
    {/each}
</div>

<style>
a:visited{
    text-decoration: none;
    color:black;
}
.margin{
margin-top:100px;
}
</style>