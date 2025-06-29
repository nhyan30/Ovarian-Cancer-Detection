using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Http;
using System.Net.Http.Headers;
using System.IO;
using Newtonsoft.Json;



namespace BackLayer
{
    public class PredictionResult
    {
        public string Class { get; set; }
        public float Confidence { get; set; }
    }

    
        public class ImagePredictor
        {
            public async Task<PredictionResult> PredictImageAsync(string imagePath)
            {
                using (var client = new HttpClient())
                using (var form = new MultipartFormDataContent())
                using (var fs = File.OpenRead(imagePath))
                using (var streamContent = new StreamContent(fs))
                {
                    streamContent.Headers.ContentType = new System.Net.Http.Headers.MediaTypeHeaderValue("image/png");
                    form.Add(streamContent, "image", Path.GetFileName(imagePath));

                    HttpResponseMessage response = await client.PostAsync("http://localhost:5000/predict", form);
                    string json = await response.Content.ReadAsStringAsync();
                    return JsonConvert.DeserializeObject<PredictionResult>(json);
                }
            }
        }

    
}
