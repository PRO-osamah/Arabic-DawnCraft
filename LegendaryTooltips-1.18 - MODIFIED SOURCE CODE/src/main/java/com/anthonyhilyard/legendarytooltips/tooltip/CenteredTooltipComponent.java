package com.anthonyhilyard.legendarytooltips.tooltip;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Matrix4f;

import net.minecraft.client.gui.Font;
import net.minecraft.client.gui.screens.inventory.tooltip.ClientTooltipComponent;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.entity.ItemRenderer;

public class CenteredTooltipComponent implements ClientTooltipComponent
{
	private final ClientTooltipComponent delegate;
	private final int targetWidth;

	public CenteredTooltipComponent(ClientTooltipComponent delegate, int targetWidth)
	{
		this.delegate = delegate;
		this.targetWidth = targetWidth;
	}

	@Override
	public int getHeight()
	{
		return delegate.getHeight();
	}

	@Override
	public int getWidth(Font font)
	{
		return Math.max(targetWidth, delegate.getWidth(font));
	}

	@Override
	public void renderText(Font font, int x, int y, Matrix4f matrix, MultiBufferSource buffer)
	{
		int actualWidth = delegate.getWidth(font);
		int centeredX = x + (getWidth(font) - actualWidth) / 2;
		delegate.renderText(font, centeredX, y, matrix, buffer);
	}

	@Override
	public void renderImage(Font font, int x, int y, PoseStack poseStack, ItemRenderer itemRenderer, int blitOffset)
	{
		delegate.renderImage(font, x, y, poseStack, itemRenderer, blitOffset);
	}
}