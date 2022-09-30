void mainImage(out vec4 fragColor, in vec2 fragCoord) {

    // Normalized pixel coordinates (from 0 to 1)
    vec2 uv = fragCoord/iResolution.xy;

    // Position of fragment relative to center of screen
    vec2 rpos = uv - 0.5;
    // Adjust y by aspect ratio
    rpos.y /= iResolution.x/iResolution.y;

    // How far is the current pixel from the origin (0, 0)
    float distance = length(rpos);
    // Use an inverse 1/distance to set the fade
    float scale = 0.02;
    float fade = 1.5;
    float strength = pow(1.0 / distance * scale, fade);

    // Fade our orange color
    vec3 color = strength * vec3(1.0, 0.5, 0.0);

    // Output to the screen
    fragColor = vec4(color, 1.0);
}